---
cite_key: fu_2023
title: DPSUR: Accelerating Differentially Private Stochastic Gradient Descent Using Selective Update and Release
authors: adding random noise, we can achieve differential privacy for a function : X → R according to Definition 2.1. The sensitivity determines how much noise is needed, is defined as follow.
year: 2024
doi: arXiv:2311.14056
url: https://arxiv.org/abs/2311.14056
relevancy: High
tldr: Novel differentially private training framework using selective gradient updates to improve convergence speed and model utility while maintaining privacy guarantees through strategic update filtering and threshold mechanisms.
insights: Proposes differentially private training framework with selective updates that evaluates gradient quality and applies only convergence-leading updates, achieving faster convergence and improved model utility compared to traditional DPSGD while maintaining privacy guarantees.
summary: This paper addresses utility loss problems in differentially private stochastic gradient descent (DPSGD) by proposing DPSUR, a framework that applies selective updates based on validation tests. The approach evaluates each gradient iteration and only applies updates that lead to convergence, discarding harmful or useless updates. The method introduces clipping strategies for update randomization and threshold mechanisms for gradient selection to ensure training proceeds in the right direction.
research_question: How can differentially private machine learning training be accelerated while maintaining privacy guarantees by selectively applying only beneficial gradient updates?
methodology: Developed DPSUR framework with gradient evaluation and selective update mechanisms; implemented clipping strategy for update randomization and threshold mechanism for gradient selection; evaluated on MNIST, FMNIST, CIFAR-10, and IMDB datasets with privacy budgets epsilon={1,2,3,4} and delta=1e-5.
key_findings: Significantly outperforms DPSGD in convergence speed and model utility across multiple datasets; demonstrates faster convergence by discarding harmful updates and focusing training in beneficial directions; maintains differential privacy guarantees.
limitations: Computational overhead from gradient evaluation and validation processes not fully characterized; scalability to larger models and datasets requires further investigation; limited evaluation to specific privacy budget ranges.
conclusion: Successfully demonstrates that selective update mechanisms can significantly improve differentially private training efficiency while maintaining strong privacy guarantees through strategic gradient filtering.
future_work: Optimize computational efficiency of validation processes; extend evaluation to larger-scale models and datasets; investigate adaptive threshold selection mechanisms.
implementation_insights: Provides practical framework for privacy-preserving model training in HDM systems, particularly relevant for training personal AI models while protecting sensitive user data through improved differential privacy mechanisms.
tags: 
---

# DPSUR: Accelerating Differentially Private Stochastic Gradient Descent Using Selective Update and Release

Jie Fu^1,^ ^2^, Qingqing Ye^2^, Haibo Hu^2^, Zhili Chen^1,^*^, Lulu Wang^1^, Kuncan Wang^1^, Xun Ran^2^

^1^Shanghai Key Laboratory of Trustworthy Computing, East China Noraml University, China
^2^Department of Electronic and Information Engineering, The Hong Kong Polytechnic University, China
jie.fu@stu.ecnu.edu.cn, qqing.ye@polyu.edu.hk, haibo.hu@polyu.edu.hk, zhlchen@sei.ecnu.edu.cn, luluwang@stu.ecnu.edu.cn, 10204804424@stu.ecnu.edu.cn, qi-xun.ran@connect.polyu.hk

## ABSTRACT

Machine learning models are known to memorize private data to reduce their training loss, which can be inadvertently exploited by privacy attacks such as model inversion and membership inference. To protect against these attacks, differential privacy (DP) has become the de facto standard for privacy-preserving machine learning, particularly those popular training algorithms using stochastic gradient descent, such as DPSGD. Nonetheless, DPSGD still suffers from severe utility loss due to its slow convergence. This is partially caused by the random sampling, which brings bias and variance to the gradient, and partially by the Gaussian noise, which leads to fluctuation of gradient updates.

Our key idea to address these issues is to apply selective updates to the model training, while discarding those useless or even harmful updates. Motivated by this, this paper proposes DPSUR, a Differentially Private training framework based on Selective Updates and Release, where the gradient from each iteration is evaluated based on a validation test, and only those updates leading to convergence are applied to the model. As such, DPSUR ensures the training in the right direction and thus can achieve faster convergence than DPSGD. The main challenges lie in two aspects privacy concerns arising from gradient evaluation, and gradient selection strategy for model update. To address the challenges, DP-SUR introduces a clipping strategy for update randomization and a threshold mechanism for gradient selection. Experiments conducted on MNIST, FMNIST, CIFAR-10, and IMDB datasets show that DPSUR significantly outperforms previous works in terms of convergence speed and model utility.

### 1 INTRODUCTION

In the past decade, deep learning techniques have achieved remarkable success in many AI tasks, such as image recognition [[32]](#ref-32), [[52]](#ref-52), [[70]](#ref-70), text analysis [[10]](#ref-10), and recommendation systems [[58]](#ref-58). However, even though the training data are not published, adversaries may still learn them by analyzing the model parameters. For example, the contents of training data can be inverted from the models [[21]](#ref-21), [[38]](#ref-38), [[43]](#ref-43), [[56]](#ref-56), [[72]](#ref-72), or the membership information of the training set can be inferred [[34]](#ref-34), [[49]](#ref-49). This is of particular concern in those applications which involve sensitive and personal data, such as medical imaging and finance. Recent legislations such as EU's General Data Privacy Regulation (GDPR) and California Consumer Privacy Act have mandated machine learning practitioners to take legal responsibility for protecting private data [[12]](#ref-12).

One of the state-of-the-art paradigms to prevent privacy disclosure in machine learning is differential privacy (DP) [[19]](#ref-19). Many works [[1]](#ref-1), [[9]](#ref-9), [[20]](#ref-20), [[25]](#ref-25), [[28]](#ref-28), [[47]](#ref-47), [[51]](#ref-51), [[59]](#ref-59) have demonstrated that by adding proper DP noise in the training phase, the resulted machine learning models can prevent unintentional leakage of private training data, such as membership inference attacks.

Among these works, the seminal work by Abadi et al. [[1]](#ref-1) proposes differentially private stochastic gradient descent (DPSGD) as the training algorithm. In DPSGD, each iteration involves four main steps: (i) randomly selecting a batch of samples using Poisson sampling, (ii) computing and clipping the gradient for each sample, (iii) adding random Gaussian noise to each gradient based on a privacy loss analysis, and (iv) updating the model weights using the average noisy gradients in the batch. In these steps, random Gaussian noise and Poisson sampling are the main reasons to cause slower convergence than conventional SGD [[57]](#ref-57), [[61]](#ref-61), [[65]](#ref-65), [[67]](#ref-67).

* (1) Gaussian Noise. In DPSGD, Gaussian noise is added to the gradient in each iteration to satisfy differential privacy. However, the noise scale can be forbiddingly large, leading to inaccurate gradient estimation and poor optimization, especially when it is close to convergence [[1]](#ref-1).
* (2) Poisson Sampling. Random sampling in SGD is usually implemented as epoch partitioning in practice. However, in DPSGD random sampling is popularly implemented as Possion sampling for its privacy amplification effect [[37]](#ref-37). Since Possion sampling may lead to bias and variance in gradient estimation, resulting in unstable and slow convergence to optimize the objective function [[6]](#ref-6), [[24]](#ref-24), [[26]](#ref-26), we attribute the performance issue of DPSGD partially to random sampling.

Although there are a few recent works which optimize random sampling or Gaussian noise separately [[31]](#ref-31), [[57]](#ref-57), [[66]](#ref-66), as shown by the blue trace in Figure 1, all these works still blindly update the model, whether or not the loss is improved in this iteration. This issue is particularly eminent when the training process approaches convergence and the magnitude of loss is small.

In this paper, we propose DPSUR, a Differentially Private Stochastic Gradient Descent training framework based on Selective Update and Releases. In essence, DPSUR only executes differentially private gradient descent if the gradient is in the correct direction to decrease loss and thus leads to a better model, as shown by the red trace in Figure. 1. This idea is inspired by simulated annealing (SA) [[27]](#ref-27), [[35]](#ref-35), where the objective function value (loss) is treated as "energy", and the differentially private model parameters obtained

^*^ Corresponding author

![Trajectory visualization of DPSGD and DPSUR schemes on a linear regression model.](_page_1_Figure_0.jpeg)

**Figure 1:** Trajectory visualization of DPSGD and DPSUR schemes on a linear regression model.

in each iteration is a random "solution". As such, we use the difference between the current and previous iteration's loss Δ as a criterion for accepting or rejecting model parameters.

Selecting those "correct" updates in DPSGD is non-trivial. First, the evaluation of gradient Δ needs to access a training set, which consumes additional privacy budgets. Second, how to set a threshold for selective update is essential as it directly affects the training performance. These two issues are closely interleaved. To address the first issue, we propose a clipping strategy to Δ, which employs a minimal clipping bound to minimize the perturbation error. For the second issue, we devise a threshold mechanism for update selection by optimizing the utility gain from selective update.

In addition, we also propose an optimization that selectively releases gradients during multiple iterations, which further reduces the privacy budget consumption. In summary, our contributions are as follows:

* We propose a new DPSUR framework for differentially private deep learning, which uses a validation test to select the model updates and ensures the gradient updates are in the correct direction. To our knowledge, this is the first work to apply selective update for model training under differential privacy.
* A clipping strategy and a threshold mechanism are devised to guarantee DP privacy and optimize utility gain, which enables a faster convergence and better accuracy than DPSGD.
* Furthermore, we propose Gaussian mechanism with selective release to reduce privacy budget consumption across iterations.
* Rigorous theoretical analysis has guaranteed differential privacy of DPSUR, together with a comprehensive empirical evaluation on four public datasets. The results confirm that DPSUR outperforms the state-of-the-art solutions in terms of model accuracy.

The rest of the paper is organized as follows. Section 2 introduces the preliminary knowledge. In Section 3, we present our method of selective update. Section 4 shows the selective release mechanism and the complete algorithm DPSUR. Privacy analysis is conducted in Section 5 and the experimental results are presented in Section 6. Section 7 introduces related work, followed the conclusion in Section 8.

### 2 PRELIMINARY KNOWLEDGE

### 2.1 Differential Privacy

Differential privacy is a rigorous mathematical framework that formally defines data privacy. It requires that a single entry in the input dataset must not lead to statistically significant changes in the output [[16]](#ref-16), [[17]](#ref-17), [[19]](#ref-19) if differential privacy holds.

Definition 2.1. (Differential Privacy [[19]](#ref-19)). The randomized mechanism provides (ε, δ)-Differential Privacy (DP), if for any two neighboring datasets D and D' that differ in only a single entry, ∀S ⊆ Range(A),

$$
Pr(A(D) \in S) < e^{\epsilon} \times Pr(A(D') \in S) + \delta. \tag{1}
$$

Here, ε > 0 controls the level of privacy guarantee in the worst case. The smaller ε, the stronger the privacy level is. The factor δ > 0 is the failure probability that the property does not hold. In practice, the value of δ should be negligible [[40]](#ref-40), [[73]](#ref-73), particularly less than 1/|D|^2^.

By adding random noise, we can achieve differential privacy for a function f: X → R according to Definition 2.1. The sensitivity determines how much noise is needed and is defined as follow.

Definition 2.2. (l^k^-Sensitivity[[17]](#ref-17)) For a function f: X → R, we define its norm sensitivity (denoted as Δf) over all neighboring datasets x, x' ∈ X^n^ differing in a single sample as

$$
\sup_{x,x' \in \mathcal{X}^n} ||f(x) - f(x')||_k \le \Delta_k f. \tag{2}
$$

In this paper, we focus on l^2^ sensitivity, i.e., || · ||2. Additionally, the following Lemma 2.3 ensures the privacy guarantee of postprocessing operations.

Lemma 2.3 (Post-processing [[19]](#ref-19)). Let M be a mechanism satisfying (ε, δ)-DP. Let f be a function whose input is the output of M. Then f(M) also satisfies (ε, δ)-DP.

### 2.2 Rényi Differential Privacy

Rényi differential privacy (RDP) is a relaxation of ε-differential privacy, which is defined on Rényi divergence as follows.

Definition 2.4. (Rényi Divergence [[54]](#ref-54)) Given two probability distributions P and Q, the Rényi divergence of order α > 1 is:

$$
D_{\alpha}(P||Q) = \frac{1}{\alpha - 1} \ln \mathbf{E}_{x \sim Q} \left[ \left( \frac{P(x)}{Q(x)} \right)^{\alpha} \right],
$$
(3)

where E~Q~ denotes the excepted value of x for the distribution Q, P(x), and Q(x) denotes the density of P or Q at x respectively.

Definition 2.5. (Rényi Differential Privacy (RDP) [[36]](#ref-36)) For any neighboring datasets x, x' ∈ X, a randomized mechanism M: X → R satisfies (α, R)-RDP if

$$
D_{\alpha}(\mathcal{M}(x)||\mathcal{M}(x')) \le R. \tag{4}
$$

The following Definition 2.6 provides a formal definition of Gaussian mechanism, and a formal RDP guarantee by it.

Definition 2.6. (RDP of Gaussian mechanism [[36]](#ref-36)) Assuming f is a real-valued function, and the sensitivity of f is μ, the Gaussian mechanism for approximating f is defined as

$$
\mathbf{G}_{\sigma}f(D) = f(D) + N\left(0, \mu^{2}\sigma^{2}\right),\tag{5}
$$

where N(0, μ^2^σ^2^) is normally distributed random variable with standard deviation σ and mean 0. Then the Gaussian mechanism with noise G satisfies (α, αμ^2^/2σ^2^) − RDP.

The following Lemma 2.7 defines the standard form for converting (α, R)-RDP to (ε, δ)-DP.

Lemma 2.7. (Conversion from RDP to DP [[3]](#ref-3)). if a randomized mechanism M: X → R satisfies (α, R)-RDP, then it satisfies(R + ln(1/(α − 1)) − (ln δ + ln α)/(α − 1), δ)-DP for any 0 < δ < 1.

### 2.3 Deep Learning with Differential Privacy

Differentially Private Stochastic Gradient Descent (DPSGD) is a widely-adopted training algorithm for deep neural networks with differential privacy guarantees. Specifically, in each iteration t, a batch of tuples B_t_ is sampled from D with a fixed probability b/|D|, where b is the batch size. After computing the gradient of each tuple x_i_ ∈ B_t_ as g_t_(x_i_) = ∇L(w_t_, x_i_), where w_t_ is model parameter for the i-th sample, DPSGD clips each per-sample gradient according to a fixed ℓ2 norm (Equation (6)).

$$
\overline{g}_t(x_i) = \text{Clip}(g_t(x_i); C)
$$
$$
= g_t(x_i) / \max\left(1, \frac{\|g_t(x_i)\|_2}{C}\right).
$$
(6)

In this way, for any two neighboring datasets, the sensitivity of the query Σ_i_∈B_t_ g_t_(x_i_) is bounded by C. Then, it adds Gaussian noise scaling with σ to the sum of the gradients when computing the batch-averaged gradients:

$$
\tilde{g}_t = \frac{1}{b} \left( \sum_{i \in \mathcal{B}_t} \overline{g}_t \left( x_i \right) + \mathcal{N} \left( 0, \sigma^2 C^2 \mathbf{I} \right) \right),\tag{7}
$$

where σ is the noise multiplier depending on the privacy budget. Last, the gradient descent is performed based on the batch-averaged gradients. Since initial models are randomly generated and independent of the sample data, and the batch-averaged gradients satisfy the differential privacy, the resulted models also satisfy the differential privacy due to the post-processing property.

Privacy accounting. Three factors determine DPSGD's privacy guarantee — the noise multiplier σ, the sampling ratio b/|D|, and the number of training iterations T. In reality, given the privacy parameters (ε, δ), we can set appropriate values for these three hyperparameters to optimize the performance. The privacy calibration process is performed using a privacy accountant: a numerical algorithm providing tight upper bounds for the given (ε, δ) as a function of the hyper-parameters [[1]](#ref-1), which in turn can be combined with numerical optimization routines to optimize one hyper-parameter given the other two. In this work we use the RDP [[36]](#ref-36) for privacy accounting. In practice, given ε, δ and at each iteration, we select α from {2, 3, ..., 64} to determine the smallest R.

## 3 DPSUR: DP TRAINING FRAMEWORK WITH SELECTIVE UPDATES AND RELEASE

In this section, we present our proposed framework DPSUR, with an overview in Section 3.1. Then two key components of DPSUR, namely, minimal clipping strategy and threshold mechanism,are introduced in Sections 3.2 and 3.3, respectively.

### 3.1 Overview

As aforementioned, DPSUR does not directly accept the model updates from each iteration due to the influence of random sampling and Gaussian noise. Therefore, we first calculate the loss of the generated model in each iteration, and then compare it with that from the last iteration to determine whether or not to accept the model update.

![The flowchart depicts an iterative model training algorithm. It details steps involving obtaining a new model using DPSGD, calculating loss differences (ΔE), applying a DP processing step, and checking a convergence condition (ΔE < Z). The algorithm iterates until a termination condition (t < T) is met, outputting the final model *w<sub>t</sub>*. The flowchart visually presents the algorithm's sequential steps and decision points.](_page_2_Figure_16.jpeg)

**Figure 2:** Workflow of DPSUR.

Figure 2 shows the workflow of DPSUR, which takes as inputs the total number of updates T, number of updates accepted t, acceptance threshold Z, and initialization model w0, executes the following steps, and outputs a final model.

* Step 1: In each iteration, we obtain a batch of tuples from the training set via Poisson sampling, and generate an intermediate model using the DPSGD algorithm.
* Step 2: We evaluate the intermediate model w_new_ and w^t-1^ on the validation batch B_v_ resampled from training set to calculate the loss J(w_new_) and J(w^t-1^).
* Step 3: We compute the difference of loss ΔE = J(w_new_) − J(w^t-1^) to evaluate the performance of intermediate model.
* Step 4: We clip ΔE and add noise to it to satisfy differential privacy, obtaining ΔE~f~.
* Step 5: Given the acceptance threshold Z, we accept update of the intermediate model and plus 1 if ΔE~f~ < Z, or reject it otherwise by reverting back to the last model w^t-1^ that was accepted for update.

Note that when t reaches the total number of updates T, we output the trained model w_t_.

Figure 3 further shows how we evaluate the model, i.e. obtaining J(w_new_) (step 2 in Figure 2). During each iteration, we first randomly sample a portion of the tuples B_t_ from the training set and perform DPSGD training to obtain a model. Then we randomly re-sample a portion of tuples from the training set as validation batch B_v_. Finally, the cross-entropy loss function is applied to the B_v_ to compute the loss of the current model. It is important to note that sampling from the training set for training and validation serves the purpose of privacy amplification. Specifically, re-sampling from the training set for model validation helps prevent overfitting. The complete DPSUR algorithm will be described in Section 4.2.

![Figure 4 illustrates "minimal clipping" in a machine learning model. It uses a flowchart showing a training dataset processed in mini-batches through a model ('dpsgd'), calculating a cross-entropy loss. A parallel validation process is also depicted. The text explains how clipping constrains changes in model parameters (ΔE), minimizing computational cost without significant impact on accuracy.](_page_3_Figure_2.jpeg)

**Figure 3:** Model evaluation framework in DPSUR.

### 3.2 Minimal Clipping

As the computation of ΔE accesses the training set (i.e., a portion of private tuples), it is necessary to perform a differential privacy operation on it. Intuitively, we can clip ΔE to a certain range [-C_v_, C_v_], and then add Gaussian noise with mean 0 and standard deviation σ_v_ * 2C_v_ to ensure differential privacy, as shown in Equation (8). Here, σ_v_ denotes the noise multiplier, and 2C_v_ is the sensitivity of the clipping operation.

$$
\widetilde{\Delta E} = \mathbf{Clip}(\Delta E; C_v) + \sigma_v \cdot 2C_v \cdot \mathcal{N}(0, 1),
$$

$$
= \min(\max(\Delta E, -C_v), C_v) + \sigma_v \cdot 2C_v \cdot \mathcal{N}(0, 1) \tag{8}
$$

However, setting an appropriate clipping bound for ΔE is challenging. A large C_v_ helps avoid loss of fidelity to the original values, but it also leads to large injected noise. A key observation here is that, to assess the quality of the current model, we can simply compare the loss of the model trained in this iteration with that of the previous iteration, i.e., ΔE = J(w_new_) − J(w^t-1^). If the loss is lower than the previous iteration, i.e., ΔE < 0, the current model is better and we accept it, otherwise we reject it. Therefore, we only need to determine whether ΔE is positive or negative, instead of its absolute value. With that said, we can use a small clipping bound for uniform clipping such that almost all ΔE are outside the interval [-C_v_, C_v_], which is illustrated by the red line in Figure 4.

$$
\overline{\Delta E} = \begin{cases} -C_v, & \Delta E \leq -C_v \\ \Delta E, & -C_v < \Delta E < C_v \\ C_v, & \Delta E \geq C_v \end{cases} \tag{9}
$$

We clip ΔE to a certain range [-C_v_, C_v_] as shown in Equation 9. If we choose C_v_ to be extremely small (e.g., C_v_ = 1e-10), we can

![The image displays a scatter plot illustrating the distribution of instances of ΔE against the value of ΔE. A vertical red line at ΔE=0 acts as a visual threshold, separating instances with positive and negative ΔE values. The plot likely demonstrates the distribution of a certain metric (ΔE) across multiple instances, showing the frequency of different ΔE values above and below zero. Its purpose is to visually represent the data distribution and highlight the significance of the zero value.](_page_3_Figure_10.jpeg)

**Figure 4:** The idea of minimal cilpping.

make almost all ΔE stay outside [-C_v_, C_v_], and the clipping process is simplified to Equation 10. Although in the worst case, there could be some value of ΔE in the interval of [-C_v_, C_v_], the probability is so small that we can ignore it without affecting our technical analysis. In practice, we can select the clipping bound to be small enough for loss value in gradient descent, e.g., C_v_ = 0.001.

$$
\overline{\Delta E} = \begin{cases} -C_v, & \Delta E < 0 \\ C_v, & \Delta E > 0 \end{cases}.
$$
(10)

So each possible value of ΔE is discretized as -C_v_ or C_v_ after our minimal clipping strategy. A small clipping bound ensures that the injected Gaussian noise is sufficiently small. Such clipping strategy can quantify the impact of the injected Gaussian noise. As plotted in Figure 5, given threshold Z (shown as the red lines), after minimal clipping and adding Gaussian noise, values of ΔE consist of two (partial) Gaussian distributions with a mean of C_v_ or -C_v_ and a standard deviation of σ_v_ * 2C_v_, respectively. The blue area represents the probability of the Gaussian distribution with a mean of C_v_ and less than threshold Z, while the orange and blue area together represents the probability of the Gaussian distribution with a mean of -C_v_ and less than threshold Z.

For a real example, let clipping bound C_v_ = 0.1 and noise level σ_v_ = 1. The results by the clipping strategy after adding noise are plotted in Figure 5a, where threshold Z = 0 is used to accept those updates whose ΔE < Z. We observe that the probability of accepting a high-quality model (ΔE < 0) is 69.1%, while the probability of accepting a low-quality model (ΔE > 0) is 30.8%. Next, we slightly move the acceptance threshold from 0 to -0.2 to investigate its impact on the acceptance probabilities. Figures 5b and 5c show the results of Z = -0.1 and Z = -0.2, respectively. We observe that, from Z = 0 to Z = -0.1, the probability of accepting a high-quality model drops much more slowly (from 69.1% to 50%) than that of accepting a low-quality model (from 30.8% to 15.9%). However, as Z further decreases, the situation is reversed, i.e., the probability of accepting a high-quality model drops quickly, which goes against the model convergence. This observation motivates us to explore an optimal threshold to maximize the utility gain from model updates.

![The image displays three probability density plots, each showing two overlapping normal distributions (μ = -C<sub>v</sub> in orange, μ = C<sub>v</sub> in blue), with shaded areas representing probability. The plots illustrate the effect of varying Z (a parameter, taking values 0, -0.1, and -0.2) on the overlap between the distributions. The purpose is to visualize the impact of Z on a specific probability calculation within the paper's context.](_page_4_Figure_0.jpeg)

**Figure 5:** The Gaussian probability distributions under different thresholds Z, where the Gaussian distribution N(μ, (2 * C_v_)^2^) and the σ_v_ = 1, C_v_ = 0.1

### 3.3 Threshold Mechanism

In this subsection, we derive an optimal threshold Z. Formally, let Z = β * C_v_. Then for the case of ΔE < 0, the CDF of the Gaussian distribution N(-C_v_, (2 * C_v_ * σ_v_)^2^) less than Z is

$$
P(X < Z) = \Phi\left(\frac{\beta \cdot C_v - (-C_v)}{2C_v \cdot \sigma_v}\right) = \Phi\left(\frac{\beta + 1}{2\sigma_v}\right),\tag{11}
$$

where X = N(-C_v_, (2 * C_v_ * σ_v_)^2^) and Φ(x) = 1/√2π ∫~-∞~^x^ e^-t^2^/2^ dt. Similarly, the CDF of the case ΔE > 0 is

$$
P(X < Z) = \Phi\left(\frac{\beta \cdot C_v - C_v}{2C_v \cdot \sigma_v}\right) = \Phi\left(\frac{\beta - 1}{2\sigma_v}\right),\tag{12}
$$

where X = N(C_v_, (2 * C_v_ * σ_v_)^2^). According to Equations (11) and (12), the parameter C_v_ will be eliminated in the CDF of Gaussian distribution, so the acceptance probability of the algorithm only depends on the parameters β and σ_v_.

In Figure 6, we plot the probabilities of accepting high-quality (ΔE < 0) and low-quality (ΔE > 0) models for popular σ_v_: 0.8, 1.0, and 1.3, with respect to β ranging from -3.5 to 0.5. Obviously, smaller β value results in decreasing probabilities of accepting both high-quality (ΔE < 0) and low-quality (ΔE > 0) models. To find a β that maximizes the difference between the two probabilities (i.e., the red dashed vertical line), we find that such β seems to be around -1.0 for all three σ_v_. As will be shown in Figure 9c of the experimental results, setting β = -1.0 does achieve excellent results in all datasets.

![The image displays a graph plotting probability against β, showing curves for different values of ΔE and σ<sub>ν</sub>. Solid lines represent ΔE > 0, while dashed lines represent ΔE < 0. Different colors represent varying σ<sub>ν</sub> values (0.8, 1, and 1.3). The graph likely illustrates the probability of an event based on these parameters, with a vertical dashed line indicating a point of interest where curves intersect. The purpose is to visually represent the impact of ΔE and σ<sub>ν</sub> on probability within the context of the paper's model.](_page_4_Figure_9.jpeg)

**Figure 6:** Acceptance probability vs. β.

Summary. To address the privacy concerns arising from the evaluation on selective update, we propose a randomized algorithm coupled with a minimal clipping strategy and a threshold mechanism. In particular, by setting a sufficiently small clipping bound (e.g., 0.001) and the acceptance threshold Z = β * C_v_, the impact of C_v_ on the selection update is eliminated according to Equations (11) and (12). Further, a suitable β is selected based on probability distributions to achieve maximum utility for selective updates.

## 4 SELECTIVE RELEASE IN DPSUR: AN OPTIMIZATION

As of now, iteratively calculating the ΔE~f~ in each iteration requires continual privacy budget consumption. In Section 4.1, we prove that by only releasing the model when a selective update occurs, DPSUR can preserve the privacy budget. Finally, we summarize the overall algorithm of DPSUR in Section 4.2.

### 4.1 Gaussian Mechanism with Selective Release

Recall that when we obtain ΔE~f~, to protect privacy, we clip ΔE in [-C_v_, C_v_] and add Gaussian noise according to Equation 8 in each iteration. According to step 5 of Figure 2, we do not update the model until ΔE~f~ exceeds the threshold Z. If we take one step further and do not release ΔE~f~ in such cases, as described in Algorithm 1, DPSUR only consumes privacy budget when a selective update occurs, i.e., ΔE~f~ < β * C_v_. In this subsection, we conduct privacy analysis to ensure Algorithm 1 can satisfy the same RDP guarantee as that of the underlying Gaussian mechanism in Definition 2.6.

In general, for the query result f(D) on dataset D, Algorithm 1 clip the f(D) in [0, μ] and adds Gaussian noise until the noisy result falls in a designated interval [a, b]. The following Theorem 4.1 shows that when a → -∞, Algorithm 1 can satisfy the same RDP guarantee.

Theorem 4.1. Algorithm 1 satisfies (α, αμ^2^/2σ^2^) − RDP when a → -∞.

Proof. Figure 7a plots two normal distributions, namely N(0, μ^2^σ^2^) and N(μ, μ^2^σ^2^), as the output probability distributions of function f on two neighboring datasets whose sensitivity is μ. By selective update and selective release in the threshold range [a, b], the probability distribution outside of this interval will accumulate within

| Algorithm 1: Gaussian mechanism with selective release |
|---|
| Input: function f(·), dataset D, Gaussian distribution N, a given interval [a, b] |
| Output: A(D) that falls in the interval [a, b] after adding Gaussian noise |
| 1 Clipping f(D) to interval [0, μ] to obtain sensitivity μ; |
| 2 A(D) = f(D) + N(0, μ^2^σ^2^); |
| 3 while A(D) < a or A(D) > b do |
| 4 A(D) = f(D) + N(0, μ^2^σ^2^); |
| 5 return A(D) |

the interval. As such, the final output distribution is truncated and transformed into a truncated normal distribution, as shown in Figure 7b. As X is assumed to follow a normal distribution, the truncated normal distribution with mean 0 and mean μ can be represented as follows:

$$
f(x; 0, \mu\sigma, a, b) = \begin{cases} \frac{1}{\mu\sigma\sqrt{2\pi}}e^{-\frac{x^2}{2\mu^2\sigma^2}} \cdot \frac{1}{\Phi\left(\frac{b}{\mu\sigma}\right) - \Phi\left(\frac{a}{\mu\sigma}\right)} & a \leq x \leq b, \\ 0 & \text{otherwise.} \end{cases}
$$

$$
f(x; \mu, \mu\sigma, a, b) = \begin{cases} \frac{1}{\mu\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\mu^2\sigma^2}} \cdot \frac{1}{\Phi\left(\frac{b-\mu}{\mu\sigma}\right) - \Phi\left(\frac{a-\mu}{\mu\sigma}\right)} & a \leq x \leq b, \\ 0 & \text{otherwise.} \end{cases}
$$

Here μσ is the standard deviation of the original normal distribution, whereas a and b are the lower and upper truncation values, respectively. Φ(x) denotes the cumulative distribution function of the standard normal distribution.

Then we substitute the two truncated normal distributions into Rényi divergence [[54]](#ref-54) to calculate the RDP as follows:

$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b))|f(x; \mu, \mu\sigma, a, b))
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; 0, \mu\sigma, a, b)]^{\alpha}}{[f(x; \mu, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma \sqrt{2\pi}} \int_{a}^{b} \exp[(-x^{2} + 2(1 - \alpha)\mu x - (1 - \alpha)\mu^{2})/(2\mu^{2}\sigma^{2})] dx\}
$$

$$
= \frac{1}{\alpha - 1} \cdot \{\frac{\alpha(\alpha - 1)}{2\sigma^{2}} + \ln[\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot (\Phi(\frac{b - (1 - \alpha)\mu}{\mu\sigma}) - \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma}))]\}
$$

$$
= \frac{\alpha}{2\sigma^{2}} + \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha}} \cdot [\Phi(\frac{b - (1 - \alpha)\mu}{\mu\sigma}) - \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma})^{\alpha}] \}
$$

$$
- \Phi(\frac{a - (1 - \alpha)\mu}{\mu\sigma})]\}, \tag{13}
$$

where Φ(x) = 1/√2π ∫~-∞~^x^ e^-t^2^/2^ dt.

![The image displays two pairs of probability density functions (PDFs). Panel (a) shows untruncated normal distributions N(0, μσ²) (gold) and N(μ, μσ²) (blue), illustrating a shift in mean. Panel (b) shows the same distributions after truncation to the interval [a, b], demonstrating the effect of truncation on the shape and scale of the PDFs. The purpose is to visually represent the impact of truncation on normal distributions within the context of a statistical analysis.](_page_5_Figure_9.jpeg)

**Figure 7:** Before and after truncating the normal distribution.

As a → -∞, we can get:

$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b) || f(x; \mu, \mu\sigma, a, b))
$$

$$
= \frac{\alpha}{2\sigma^2} + \frac{1}{\alpha - 1} \cdot \ln\left[\frac{(\Phi(\frac{b - \mu}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b}{\mu\sigma}))^{\alpha}} \cdot \Phi(\frac{b + (\alpha - 1)\mu}{\mu\sigma})\right]
$$
(14)

Similarly, we can get :

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b))|f(x; 0, \mu\sigma, a, b))
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; \mu, \mu\sigma, a, b)]^{\alpha}}{[f(x; 0, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$

$$
= \frac{1}{\alpha - 1} \cdot \left\{ \frac{\alpha(\alpha - 1)}{2\sigma^{2}} + \ln \left[ \frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b - \mu}{\mu\sigma}) - \Phi(\frac{a - \mu}{\mu\sigma}))^{\alpha}} \right] \right\}
$$

$$
\cdot (\Phi(\frac{b - \alpha\mu}{\mu\sigma}) - \Phi(\frac{a - \alpha\mu}{\mu\sigma}))]
$$

$$
= \frac{\alpha}{2\sigma^{2}} + \frac{1}{\alpha - 1} \cdot \ln \left[ \frac{(\Phi(\frac{b}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b - \mu}{\mu\sigma}))^{\alpha}} \cdot \Phi(\frac{b - \alpha\mu}{\mu\sigma}) \right]
$$

According Theorem 4.2, we have:

$$
D_{\alpha}(f(x; 0, \mu\sigma, a, b)||f(x; \mu, \mu\sigma, a, b)) \leq \alpha/2\sigma^{2}, and
$$

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)||f(x; 0, \mu\sigma, a, b)) \leq \alpha/2\sigma^{2}.
$$

Therefore, Theorem 4.1 is proved. The details of RDP of two truncated normal distributions are presented in Appendix A. □

Next, we will prove Theorem 4.2. This theorem is an inequality proof of the cumulative distribution function (CDF) of the normal distribution, and it provides the foundation for the proof of Theorem 4.1.

THEOREM 4.2. If
$$
A = (\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b+(\alpha-1)\mu}{\mu\sigma})/(\Phi(\frac{b}{\mu\sigma}))^{\alpha}, B = (\Phi(\frac{b}{\mu\sigma}))^{\alpha-1} \cdot \Phi(\frac{b-\alpha\mu}{\mu\sigma})/(\Phi(\frac{b-\mu}{\mu\sigma}))^{\alpha}
$$
, where $\Phi(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{x} e^{-\frac{t^2}{2}} dt$ .
A, $B \le 1$ , when $\mu > 0$ , $\sigma > 0$ and $\alpha > 1$ .

Proof. The second derivative of ln [Φ(x)] is:

$$
\ln''\left[\Phi(x)\right] = \frac{\Phi''(x) \cdot \Phi(x) - \Phi'(x) \cdot \Phi'(x)}{[\Phi(x)]^2}
$$
$$
= \frac{-x \cdot \Phi'(x) \cdot \Phi(x) - \Phi'(x) \cdot \Phi'(x)}{[\Phi(x)]^2},
$$
(16)

where Φ'(x) = 1/√2π e^-x^2^/2^. When x ≥ 0, since Φ(x), Φ'(x) > 0, ln''[Φ(x)] < 0 always hold.

When x < 0, Φ'(x) > 0. As such, proving -x * Φ'(x) * Φ(x) - Φ'(x) * Φ'(x) < 0 is equivalent to proving -x * Φ(x) - Φ'(x) < 0. We let K(x) = -x * Φ(x) - Φ'(x), so the derivative for K(x) is:

$$
K'(x) = -\Phi(x) + (-x) \cdot \Phi'(x) - \Phi''(x)
$$

$$
= -\Phi(x) + (-x) \cdot \Phi'(x) - (-x) \cdot \Phi'(x) \tag{17}
$$
$$
= -\Phi(x) < 0
$$

Since lim~x→-∞~ K(x) = 0, K(x) < 0 when x < 0. In summary, ln''[Φ(x)] < 0 always holds. In other words, ln''[Φ(x)] is the concave function when x ∈ (-∞, ∞). According to the properties of the concave function, we can obtain:

$$
\lambda \cdot \ln \left[ \Phi(x_1) \right] + (1 - \lambda) \ln \left[ \Phi(x_2) \right] \le \ln \left[ \Phi(\lambda x_1 + (1 - \lambda) x_2) \right],
$$

where λ ∈ (0, 1) and x1, x^2^ ∈ (-∞, ∞).

Let λ = (α - 1)/α (α > 1), x^1^ = (b - μ)/μσ, x^2^ = (b + (α - 1)μ)/μσ or x^1^ = b/μσ, x^2^ = (b - αμ)/μσ. Then the following two inequalities hold:

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

where $\mu, \sigma > 0$ and $\alpha > 1$ . (19)

Theorem 4.2 is proved. □

This proves Algorithm 1 satisfies the same (α, αμ^2^/2σ^2^)-RDP as Gaussian mechanism of RDP [[36]](#ref-36). In other words, DPSUR only consumes privacy budget when the update is selected and released based on the interval. As such, in Figure 2, the privacy budget of computing ΔE~f~ is consumed only if ΔE~f~ < Z.

### 4.2 DPSUR: Putting Things Together

Now we describe the overall algorithm of DPSUR in Algorithm 2, which consists of the following two steps.

i. DPSGD (Lines 3-8). This part is the traditional DPSGD procedure. First, a small batch of samples B_t_ are randomly selected from the training datasets (Line 3). For each sample x_i_ ∈ B_t_, its gradient values are calculated and clipped so that the l^2^ norm of the gradients is not greater than the clipping bound C_t_ (Lines 4-6). In Line 7, the clipped gradients are first summed up, and then added Gaussian noise N(0, σ_t_^2^C_t_^2^) to satisfy differential privacy, and finally averaged. As such, the sensitivity is C_t_ here. Gradient descent is then performed using these noisy gradients to obtain a new temporary model w_new_ for the current iteration (Line 8).

ii. Selective update (Lines 9-18). First, a small batch of samples B_v_ are randomly selected from the training set (Line 9). Then we calculate the loss for temporary model J(w_new_) and the latest accepted model J(w^t-1^), where J(w_new_) = 1/|B_v_| Σ_x_i_∈B_v_ L(w_new_, x_i_), and subtract them to get ΔE (Lines 10-11). To get the sensitivity, ΔE is clipped to [-C_v_, C_v_], which means that one less or one more sample

produces a maximum variation of 2C_v_ for ΔE (Line 12). To ensure differential privacy, Gaussian noise N(0, σ_v_^2^ * (2C_v_)^2^) is added to obtain a noisy version ΔE~f~ (Lines 13). The temporary model will be accepted and plus 1 if ΔE~f~ < β * C_v_, where β is the acceptance threshold parameter (Lines 15-16). Otherwise, the temporary model is rejected, and the model from the last iteration is returned (Line 18).

The above two steps are repeated until the entire privacy budget is consumed. We will provide rigorous privacy analysis in the next section.

## Algorithm 2: Overall algorithm of DPSUR

| | Input: training datasets {x1, x2, ..., xN}, loss function |
|---|---|
| | L(θ, x). Parameters: learning rate η, batch size for |
| | training B_t_, noise multiplier for training σ_t_, clipping |
| | bound for training C_t_, batch size for validation B_v_, |
| | noise multiplier for validation σ_v_, clipping bound for |
| | validation C_v_, threshold parameter β |
| | Output: the final trained model w_t_ |
| 1 | Initialize t = 1, w0 = Initial(); |
| 2 | while t < T do |
| 3 | Randomly sample a batch B_t_ with probability B_t_/N; |
| 4 | for x_i_ ∈ B_t_ do |
| 5 | Compute g_t_(x_i_) ← ∇L(w_t_,x_i_); |
| 6 | g_t_(x_i_) ← g_t_(x_i_)/max(1, ||g_t_(x_i_)||2/C_t_); |
| 7 | g~e~_t_ ← (1/|B_t_|) (Σ_i_∈B_t_ g_t_(x_i_) + N(0, σ^2^C_t_^2^)); |
| 8 | w_new_ = w^t-1^ − η_t_g~e~_t_; |
| 9 | Poisson sampling a batch B_v_ with probability B_v_/N; |
| 10 | Compute loss J(w_new_) and J(w^t-1^) by batch B_v_; |
| 11 | ΔE = J(w_new_) − J(w^t-1^); |
| 12 | ΔE = min(max(ΔE, −C_v_),C_v_); |
| 13 | ΔE~f~ = ΔE + N(0, σ_v_^2^ · (2C_v_)^2^); |
| 14 | if ΔE~f~ < β · C_v_ then |
| 15 | w_t_ = w_new_; |
| 16 | t = t + 1; |
| 17 | else |
| 18 | w_t_ = w^t-1^; |
| 19 | return w_t_ |

### 5 PRIVACY ANALYSIS

This section establishes the privacy guarantee of DPSUR. Since DP-SUR is non-interactive, it only releases the final model accumulated from all accepted model updates. In the following, we first analyze the privacy loss of each accepted model update, and then derive the total privacy loss based on sequential composition.

For each accepted model update in Algorithm 2, there are only two places where the raw training data is accessed. One is the computation of model updates in the training phase, and the other is the computation of test values ΔE~f~ in the validation phase. As shown in Figure 8, the model update and test value sequences are in the form of "rejected, ..., rejected, accepted".

In the validation phase, the computation of each test value ΔE~f~ takes as input the training set and the corresponding model update w_new_, and the latter is a function of the training set. Due to the function composition, the computation of ΔE~f~ can be regarded as a function of the training set whose output is a value in [-C_v_, C_v_]. Therefore, Line 13 in Algorithm 2 ensures that the computation satisfies differential privacy due to the Gaussian mechanism. Furthermore, computing and testing the values ΔE~f~ until one value is accepted satisfies the same differential privacy according to Theorem 4.1.

In the training phase, since the accepted model update is selected solely based on the test value ΔE~f~ which satisfies differential privacy, the model update selection satisfies differential privacy due to the post-processing property. Additionally, all rejected model updates are never released and thus consume no privacy budget, even though they have been computed. Therefore, the privacy loss in the training phase comes only from the computation of accepted model updates.

Based on the above analysis, we will use the Rényi Differential Privacy (RDP) approach to calculate the privacy loss in the training and validation phases in Sections 5.1 and 5.2 respectively, compose them sequentially, and finally convert the RDP into (ε, δ)-DP in Section 5.3.

![The image displays a diagram illustrating a process divided into training, validation, and release phases. Two sequences (1 and *t*) are shown, each involving multiple weight vectors (*w<sub>i</sub>*) and their associated error terms (ΔE<sub>i</sub>). The diagram depicts a sequential computation, where intermediate results undergo operations labeled 'RU' and 'AU' before final release. A separate equation defines *A<sub>α</sub>*, likely a key parameter within the described process.](_page_7_Figure_3.jpeg)

**Figure 8:** The privacy analysis of DPSUR. (RU: Rejected Update, AU: Accepted Update)

### 5.1 Privacy Analysis of Training

As mentioned above, the RDP of the training phase is only resulted from the accepted model updates. Theorem 5.1 gives the proof of RDP in the training phase.

Theorem 5.1. After accepting t model updates, the RDP of the training phase of DPSUR satisfies:

$$
R_{train}(\alpha) = \frac{t}{\alpha - 1} \ln \left[ \sum_{i=0}^{\alpha} \begin{pmatrix} \alpha \\ i \end{pmatrix} (1 - q)^{\alpha - i} q^i \exp \left( \frac{i^2 - i}{2\sigma_t^2} \right) \right],
$$
(20)

where q = b/N, σ_t_ is noise multiplier of the training phase, and α > 1 is the order.

Proof. We will prove this in the following two steps: (i) use the RDP of the sampling Gaussian mechanism to calculate the privacy cost of each accepted model update, which relies on Definitions 5.2 and 5.3, and (ii) use the composition of RDP mechanisms to compute the privacy cost of multiple accepted model updates by Lemma 5.4.

Definitions 5.2 and 5.3 define Sampled Gaussian Mechanism (SGM) and its Rényi Differential Privacy (RDP), respectively.

Definition 5.2. (Sampled Gaussian Mechanism (SGM) [[37]](#ref-37)). Let f be a function mapping subsets of D to R^d^. We define the Sampled Gaussian Mechanism (SGM) parameterized with the sampling rate 0 < q ≤ 1 and the σ > 0 as

$$
SG_{q,\sigma}(S) \triangleq f(\lbrace x : x \in S \text{ is sampled with probability } q \rbrace)
$$

$$
+\, \mathcal{N}\left(0, \sigma^2 \mathbb{I}^d\right). \tag{21}
$$

In DPSUR, f(S) is the clipped gradient evaluation on sampled data points f({x_i_}∈S) = Σ_x_i_∈S g_t_(x_i_). If f(S) is obtained by clipping with a gradient norm bound C, then the sensitivity of f(S) is C.

Definition 5.3. (RDP privacy budget of SGM [[37]](#ref-37)). Let SG_q,σ_ be the Sampled Gaussian Mechanism for some function f. If f has a sensitivity of 1, SG_q,σ_ satisfies (α, R)-RDP if

$$
R \le \frac{1}{\alpha - 1} \ln[ max(A_{\alpha}(q, \sigma), B_{\alpha}(q, \sigma)) ], \tag{22}
$$

where

$$
\begin{cases} A_{\alpha}(q,\sigma) \triangleq \mathbb{E}_{z \sim \mu_0} [(\mu(z)/\mu_0(z))^{\alpha}] \\ B_{\alpha}(q,\sigma) \triangleq \mathbb{E}_{z \sim \mu} [(\mu_0(z)/\mu(z))^{\alpha}] \end{cases}
$$
(23)

with μ^0^ ≜ N(0, σ^2^), μ^1^ ≜ N(1, σ^2^) and μ ≜ (1 − q)μ^0^ + qμ^1^.

Furthermore, it holds for ∀(q, σ) ∈ (0, 1]×R^+, R(α, q, σ) ≥ R(α, q, σ). Thus, SG_q,σ_ satisfies (α, 1/(α − 1) ln (A_α_(q, σ))) -RDP.

Finally, the existing work [[37]](#ref-37) describes a procedure to compute A_α_(q, σ) depending on integer α as Eq. (24).

$$
A_{\alpha} = \sum_{k=0}^{\alpha} \binom{\alpha}{k} (1-q)^{\alpha-k} q^k \exp\left(\frac{k^2 - k}{2\sigma^2}\right) \tag{24}
$$

Lemma 5.4 shows the composition property of RDP mechanisms.

Lemma 5.4. (Composition of RDP [[36]](#ref-36)). For two randomized mechanisms M1, M2, such that M1 is (α, R1)-RDP and M2 is (α, R2)-RDP the composition of M1 and M2 which is defined as (M1, M2)(a sequence of results), where M1 ∼ D1 and M2 ∼ D2, satisfies (α, R1 + R2) − RDP.

According to Definitions 5.2 and 5.3, and Lemma 5.4, Theorem 5.1 is proved.

□

### 5.2 Privacy Analysis of Validation

As Section 4.1 mentioned above, the RDP of validation will be accumulated only when ΔE~f~ < β * C_v_.

Theorem 5.5. After accepting t tests of ΔE~f~, the RDP of the validation phase satisfies:

$$
R_{valid}(\alpha) = \frac{t}{\alpha - 1} \ln \left[ \sum_{i=0}^{\alpha} \left( \begin{array}{c} \alpha \\ i \end{array} \right) (1 - q)^{\alpha - i} q^i \exp \left( \frac{i^2 - i}{2\sigma_v^2} \right) \right], (25)
$$

where q = b/N, σ_v_ is noise multiplier of the validation phase, and α > 1 is the order.

The proof is similar to that of the training phase, so we omit it.

### 5.3 Overall Privacy Analysis of DPSUR

Since both training and validation phases access the same training set, we need to combine their RDPs sequentially using Lemma 5.4, and then use Lemma 2.7 to convert it to (ε, δ)-DP. Therefore, the final privacy loss of DPSUR is as follows:

Theorem 5.6. (Privacy loss of DPSUR). The privacy loss of DPSUR satisfies:

$$
(\epsilon, \delta) = (R_{train}(\alpha) + R_{valid}(\alpha) + \ln((\alpha - 1)/\alpha) - (\ln \delta + \ln \alpha)/(\alpha - 1), \delta),
$$
(26)

where 0 < δ < 1, R_train_(α) is the RDP of training which is computed by Theorem 5.1, and R_valid_(α) is the RDP of validation which is computed by Theorem 5.5.

### 5.4 Discussion of Privacy

Our privacy analysis shows that DPSUR strictly adheres to the principles of differential privacy, limiting adversaries to conduct differential attacks solely based on the algorithm's output. However, it is worth noting that DPSUR may be susceptible to interactive side-channel attacks. For instance, a strong adversary (e.g., the hypervisor of a guest OS in the cloud) who has access to DPSUR's internal update/release status could measure the time interval of two adjacent model updates to infer the number of rejections in between and thus cause privacy breaches. To mitigate such threats, we suggest introducing random waiting time for update acceptance cases. Nonetheless, we emphasize that DPSGD is supposed to work in a non-interactive training scenario where the attacker can only access the final output model. Since most real-world machine learning systems are non-interactive during training, the privacy guarantee provided by DPSUR remains sufficient and consistent with other DPSGD variants.

To further validate such privacy guarantee in real-world scenarios, in Section 6.4 we conduct membership inference attacks on the trained models. The experimental results indicate that DPSUR exhibits strong defense against membership inference attacks, thus safeguarding the privacy of training data.

### 6 EXPERIMENTAL EVALUATION

In this section, we conduct experiments to demonstrate the performance of DPSUR over four real datasets and popular machine learning models. And we perform experiments involving two member inference attacks to show the privacy-preserving effect of DPSUR. All experiments are implemented in Python using Py-Torch [[45]](#ref-45). Codes to reproduce our experiments are available at [https://github.com/JeffffffFu/DPSUR](https://github.com/JeffffffFu/DPSUR).

### 6.1 Experimental Setting

6.1.1 Baseline. We compare DPSUR with DPSGD [[1]](#ref-1) and four state-of-the-art variants, namely DPSGD with important sampling [[57]](#ref-57), handcrafted features [[53]](#ref-53), tempered sigmoid activation [[41]](#ref-41), and adaptive learning rate [[31]](#ref-31), which we refer to as DPSGD-IS, DPSGD-HF, DPSGD-TS, and DPAGD respectively. Note that we do not compare DPSUR with those approaches that modify the structures of over-parameterized models [[13]](#ref-13) or the semi-supervised model PATE [[39]](#ref-39), [[40]](#ref-40), as they differ significantly from the scope of this work.

6.1.2 Datasets and Models. Experimental evaluation is conducted over three image classification datasets, including MNIST [[30]](#ref-30), Fashion MNIST (FMNIST) [[60]](#ref-60), and CIFAR-10 [[29]](#ref-29), and a movie review dataset IMDB [[33]](#ref-33).

MNIST contains 60,000 training samples and 10,000 testing samples of handwritten digits, divided into 10 categories with 7,000 grayscale images per category. Each sample consists of a grayscale image of size 28 × 28 and a corresponding label indicating its category. The model trained using handcrafted features as inputs achieves 99.11% accuracy after 20 epochs in the non-private setting [[53]](#ref-53).

FMNIST consists of 60,000 training samples and 10,000 testing samples of fashion products categorized into 10 categories, with each category containing 7,000 grayscale images of size 28×28. The dataset also includes labels indicating the category of each image. The model trained using handcrafted features as inputs achieves 90.98% accuracy after 20 epochs in the non-private setting [[53]](#ref-53).

CIFAR-10 comprises 50,000 training samples and 10,000 testing samples of colored objects categorized into 10 categories. Each category contains 6,000 color images of size 32 × 32 with three color channels. Additionally, each sample is accompanied by a label indicating the category to which it belongs. The model trained using handcrafted features as inputs achieves 71.12% accuracy after 20 epochs in the non-private setting [[53]](#ref-53).

IMDb consists of 50,000 reviews of movies, each review encoded as a list of word indexes and labeled with an obvious bias towards either positive or negative sentiment. The dataset is divided into a training set of 25,000 reviews and a test set of 25,000 reviews. In the non-private setting, the model trained using cross-entropy loss function, Adam optimizer, and an expected batch size of 32 achieves an accuracy of 79.97% after 20 epochs.

We apply the same convolutional neural network architecture as [[41]](#ref-41), [[53]](#ref-53), [[57]](#ref-57) to three image datasets, i.e., MNIST, FMNIST, and CIFAR-10. Additionally, we used a same five-layer recurrent neural network as in [[57]](#ref-57) for the IMDB dataset. We use the categorical cross-entropy loss function for all datasets. The details of model architectures are presented in Appendix B.

**Table 1:** Noise multiplier for validation

| Dataset | ε = 1 | ε = 2 | ε = 3 | ε = 4 |
|---|---|---|---|---|
| MNIST | 1.3 | 1.0 | 0.9 | 0.8 |
| FMNIST | 1.3 | 1.3 | 0.8 | 0.8 |
| CIFAR-10 | 1.3 | 1.3 | 1.1 | 1.1 |
| IMDB | 1.3 | 1.2 | 1.0 | 0.9 |

6.1.3 Parameter Settings. In our experiments, we set the privacy budget ε from 1 to 4 for each dataset while fixing δ = 10^-5^. For image datasets, we user the SGD optimizer with a momentum parameter set to 0.9; for the IMDB dataset, we employ the Adam optimizer whose parameters are the same as [[11]](#ref-11).

During the DPSGD phase, for the three image datasets, we adopt the best parameters recommended in [[53]](#ref-53). Specifically, we finetune the noise multiplier for various ε, following the approach outlined in [[53]](#ref-53), [[57]](#ref-57). This fine-tuning process is a common practice in all privacy-preserving machine learning methods, and it does not incur any privacy loss. For the IMDB dataset, we enumerate different values and choose the best for each parameter since the competitor method [[57]](#ref-57) does not specify them.

Based on our analysis in Section 3.2 and 3.3, we set the clipping bound C_v_ = 0.001 for ΔE and acceptance parameter β = -1 to all privacy budgets and datasets. In addition, for MNIST, FMNIST and CIFAR-10, we set the batch size of validation set B_v_ = 256. While IMDB, which have fewer training samples, we set the batch size of validation set B_v_ = 128. The noise multiplier for validation σ_v_ ranges from 0.8 to 1.3 for all datasets and privacy budgets, as shown in Table 1. Intuitively, when the privacy budget is small, we increase σ_v_ to add more iteration rounds.

### 6.2 Overall Performance

Table 2 shows the classification accuracies of DPSUR and five competitive methods. It is noteworthy that DPSUR consistently outperforms all competitors across all datasets and privacy budgets, except for a less eminent advantage on the MNIST dataset where the accuracy of [[57]](#ref-57) already approaches that of the non-private setting, leaving little room for further improvement. For the other three datasets, the classification accuracy of DPSUR is at least 1% higher than the second best, which shows a huge improvement over DPSGD.

Notably, DPSUR performs almost as well as in the non-private setting at ε = 4 in three image datasets. The superior performance of the DPSUR is attributed to our objective of selecting model updates to minimize the loss function. Moreover, We derive the RDP for the selective Gaussian mechanism, which allows us to reduce the consumption of privacy loss. In particular, on the CIFAR-10 dataset, we observe that DPSUR even outperforms non-private results when ε = 4. This is because moderate noise in SGD sometimes helps the neural network escape from local minima [[22]](#ref-22).

### 6.3 Impact of Various Parameters

In this subsection, we study the impact of various parameters of DPSUR, including the learning rate, the noise multiplier of validation, the cilpping bound of loss, and the threshold parameter. Due to space limitation, we only show the results of CIFAR-10 dataset. In all experiments, if not specified, we use the SGD optimizer with the momentum 0.9, and set the learning rate η = 4.0, batch size for training B_t_ = 8192, noise multiplier for training σ_t_ = 5.67, batch size for validation B_v_ = 128, noise multiplier for validation σ_v_ = 1.1, clipping bound for validation C_v_ = 0.001, the threshold parameter β = −1, and privacy budget (ε=3, δ=10^-5^).

Learning rate η. As plotted in Figure 9a, the highest accuracy achieved is 70.83% when using a learning rate of η = 4. If the learning rate is larger than 4, the accuracy starts to decrease. This is because a large learning rate may cause slow convergence to the trained model. However, thanks to selective update, DPSUR becomes adaptive to different learning rates, and the accuracy remains stable at 70.02% when using a extremely high learning rate η = 7.

Noise multiplier for validation σ_v_. A large σ_v_ can save privacy budget running more rounds, which degrades the quality of the accepted model. On the contrary, a small σ_v_ can guarantee the accepted model quality, but consumes more privacy budget. According to Figure 9b, we find that the test accuracy of DPSUR is

quite stable at around 70.3% when σ_v_ increases from 0.8 to 1.3, and the highest accuracy is 70.83% when σ_v_ = 1.1.

Clipping bound for validation C_v_. As aforementioned, using a sufficiently small clipping bound can discretize the difference of the loss ΔE. With a shallow model training on CIFAR-10, loss values ranging from 0.01 to 0.0001 are all considered sufficiently small, a smaller C_v_ (e.g. 1e-05) than the front does not bring performance gains. As shown in Figure 9c, the accuracy for the cases of C_v_ ∈ [0.01, 1e-05] achieves slightly better performance. However, when C_v_ is set to 1 or 10, we observe a significant decline in performance, which is consistent with our analysis that setting a large C_v_ does not provide any performance benefits.

Threshold parameter β. The acceptance probability is influenced by the parameter β, with smaller values leading to a decreasing probability of accepting both low-quality and high-quality models. As shown in Figure 9d, the best performance is achieved when β = −1.0. This is consistent with our analysis in Section 3.3 that a smaller β leads to a higher rejection probability for lowquality updates, thereby guiding the model towards the correct direction during iterations. It is worth noting that setting β too small does not gain more benefits, as a very small β causes the model to reject almost all high-quality and low-quality solutions, contributing nothing to the model convergence.

Batch size of validation set B_v_. A small B_v_ can help conserve the privacy budget, enabling more rounds of computation. However, this can result in a decrease in the quality of the accepted model. Conversely, a larger value of B_v_ can ensure better model quality but consumes a greater portion of the privacy budget. As shown in Figure 9e, we observe that as B_v_ increases from 32 to 256, the test accuracy of DPSUR improves from 69.10% to 70.83%, but it declines to 68.36% when B_v_ = 1024.

## 6.4 Resilience Against Member Inference Attacks

Differential privacy protection is naturally resistant to membership inference attacks. To empirically verify if DPSUR achieves the same privacy guarantee as DPSGD, we conduct membership inference attacks on models trained on FMNIST and CIFAR-10, where their models are trained from DPSUR and DPSGD algorithms, respectively.

6.4.1 Attack overview. We adopt two membership inference attacks, Black-Box/Shadow [[46]](#ref-46) and White-Box/Partial [[38]](#ref-38), which are the SOTA methods in membership inference attack to our knowledge.

Black-Box/Shadow. In the Black-Box/Shadow attack scenario, the adversary has a shadow auxiliary dataset. The dataset is divided into two parts, with one part used to train a shadow model for the same task. The shadow model is then queried using the entire shadow dataset. For each query sample, the shadow model provides its posterior probability and predicted label. The adversary labels the sample as a member if it belongs to the training set of the shadow model, otherwise, it is labeled as a non-member. Using this labeled dataset, the adversary trains an attack model, which serves as a binary classifier to distinguish between members and nonmembers. To determine if a sample belongs to the target model's training dataset, it is inputted into the target model for prediction.

Since the scattering network used in DPSGD-HF [[53]](#ref-53) is not applicable to natural language processing, we omit the results of this method on the IMDb dataset.

**Table 2:** Results of classification accuracy

| Dataset | Method | ε = 1 | ε = 2 | ε = 3 | ε = 4 | non-private |
|---|---|---|---|---|---|---|
| MNIST | DPSUR | 97.93% | 98.70% | 98.88% | 98.95% | |
| (Image Dataset) | DPIS [[57]](#ref-57) | 97.79% | 98.51% | 98.62% | 98.78% | |
| | DPSGD-HF [[53]](#ref-53) | 97.78% | 98.39% | 98.32% | 98.56% | 99.11% |
| | DPSGD-TS [[41]](#ref-41) | 97.06% | 97.87% | 98.22% | 98.51% | |
| | DPAGD [[31]](#ref-31) | 95.91% | 97.30% | 97.52% | 97.83% | |
| | DPSGD [[1]](#ref-1) | 95.11% | 96.10% | 96.82% | 97.25% | |
| FMNIST | DPSUR | 88.38% | 89.34% | 89.71% | 90.18% | |
| (Image Dataset) | DPIS [[57]](#ref-57) | 86.25% | 88.24% | 88.82% | 89.21% | |
| | DPSGD-HF [[53]](#ref-53) | 85.54% | 87.96% | 89.01% | 89.06% | 90.98% |
| | DPSGD-TS [[41]](#ref-41) | 83.63% | 85.33% | 86.29% | 86.86% | |
| | DPAGD [[31]](#ref-31) | 81.26% | 84.50% | 86.04% | 86.78% | |
| | DPSGD [[1]](#ref-1) | 80.25% | 82.63% | 84.72% | 85.40% | |
| CIFAR-10 | DPSUR | 64.41% | 69.40% | 70.83% | 71.45% | |
| (Image Dataset) | DPIS [[57]](#ref-57) | 63.23% | 67.94% | 69.63% | 70.55% | |
| | DPSGD-HF [[53]](#ref-53) | 63.15% | 66.55% | 69.35% | 70.28% | 71.12% |
| | DPSGD-TS [[41]](#ref-41) | 51.52% | 56.78% | 60.42% | 61.75% | |
| | DPAGD [[31]](#ref-31) | 45.78% | 53.30% | 56.21% | 60.31% | |
| | DPSGD [[1]](#ref-1) | 46.03% | 51.33% | 54.67% | 58.89% | |
| IMDb | DPSUR | 66.50% | 71.02% | 72.16% | 74.14% | |
| (Text Dataset) | DPIS [[57]](#ref-57) | 63.56% | 66.11% | 68.49% | 70.12% | |
| | DPSGD-TS [[41]](#ref-41) | 65.08% | 68.34% | 70.10% | 70.85% | 79.97% |
| | DPAGD [[31]](#ref-31) | 58.72% | 63.48% | 64.59% | 66.01% | |
| | DPSGD [[1]](#ref-1) | 64.13% | 68.55% | 70.41% | 71.57% | |

![The image presents five line graphs (a-e) illustrating the impact of hyperparameter tuning on a DPSUR model's test accuracy. Each graph plots test accuracy (%) against a different hyperparameter: learning rate (η), noise multiplier (σ<sub>v</sub>), clipping bound (C<sub>v</sub>), threshold parameter (β), and validation set batch size (B<sub>v</sub>). The purpose is to show the model's sensitivity to these parameters and to guide optimal hyperparameter selection for improved performance.](_page_10_Figure_2.jpeg)

**Figure 9:** The impact of different parameters on the test accuracy in CIFAR-10.

The resulting posterior probability and predicted label (converted into a binary indicator of prediction correctness) are then fed into the attack model.

White-Box/Partial. In the White-Box/Partial attack scenario, the adversary has partial training dataset as the auxiliary dataset. One advantage in the White-Box/Partial attack is that the adversary has access to the target model. This allows adversary to utilize various resources, including gradients with respect to model parameters, embeddings from intermediate layers, classification loss, as well as posterior probabilities and labels of the target samples.

6.4.2 Attack setting. For each dataset, we randomly split it into four subsets: the target training dataset, target testing dataset, shadow training dataset, and shadow testing dataset. The ratio of the sample sizes in each subset is 2:1:2:1. Our target model and training parameters are consistent with those described above.

6.4.3 Results. Table 3 and Table 4 report the accuracy of two inference attacks against target models protected by DPSUR and DPSGD on FMNIST and CIFAR-10, respectively. We observe that member inference attacks are quite effective against the non-private methods (non-dp), especially on CIFRA-10. As for the two DP algorithms, the attack accuracy drops from 0.58 to around 0.50 on the FMNIST, and drops from 0.73 to around 0.50 on the CIFAR-10, which almost equals to random guess. It's noteworthy that the attack performance on FMNIST is consistently poor, as models trained on FMNIST generalize well on non-member data samples [[48]](#ref-48). These results show that the model under DP protection can defend very well against membership inference attacks, and our DPSUR algorithm can provide the same level of privacy protection as DPSGD.

**Table 3:** Accuracy of Member Inference Attack on FMNIST

| Attack | Algorithm | ε = 1 | ε = 2 | ε = 3 | ε = 4 | non-private |
|---|---|---|---|---|---|---|
| Black Box/Shadow | DPSUR | 0.498 | 0.500 | 0.503 | 0.506 | 0.582 |
| | DPSGD | 0.498 | 0.503 | 0.493 | 0.494 | |
| White Box/Partial | DPSUR | 0.499 | 0.504 | 0.501 | 0.502 | 0.584 |
| | DPSGD | 0.501 | 0.502 | 0.502 | 0.505 | |

**Table 4:** Accuracy of Member Inference Attack on CIFAR-10

| Attack | Algorithm | ε = 1 | ε = 2 | ε = 3 | ε = 4 | non-private |
|---|---|---|---|---|---|---|
| Black Box/Shadow | DPSUR | 0.495 | 0.498 | 0.503 | 0.504 | 0.732 |
| | DPSGD | 0.504 | 0.505 | 0.504 | 0.505 | |
| White Box/Partial | DPSUR | 0.499 | 0.501 | 0.502 | 0.503 | 0.743 |
| | DPSGD | 0.500 | 0.501 | 0.501 | 0.503 | |

### 7 RELATED WORK

Privacy-preserving model training was first proposed in [[5]](#ref-5), [[50]](#ref-50). Subsequently, Abadi et al. [[1]](#ref-1) proposed a generalized algorithm, DPSGD, for deep learning with differential privacy, and since then many works aimed at improving DPSGD from different aspects.

Gradient clipping. At each iteration of training, Zhang et al. [[68]](#ref-68) used public data to obtain an approximate bound on gradient norm and clip the gradients at this approximate bound. The work in [[55]](#ref-55) proposed adaptive clipping in each layer of the neural network. Andrew et al. [[2]](#ref-2) designed a method for adaptively tuning the clipping threshold to track a given quantile of the update norm distribution during training, especially in federated learning. Venkatadheeraj et al. [[44]](#ref-44) proposed AdaCliP, which using coordinate-wise adaptive clipping of the gradient. However, a recent work [[62]](#ref-62) has shown that by redefining the clipping equation as g_t_(x_i_) = g_t_(x_i_)/||g_t_(x_i_)||2, clipping is actually equivalent to normalization by setting the clipping bound small enough.

Our paper does not employ any adaptive clipping technique during the training phase. Instead, our minimal clipping is orthogonal to theirs as it is for threshold evaluation in the validation phase, not the training phase.

Gaussian noise. The work of [[42]](#ref-42) implemented adaptive noise addition using a hierarchical correlation propagation protocol approach, adding a small amount of noise to features with high correlation to the model's output. Balle and Wang [[4]](#ref-4) introduced an optimized Gaussian mechanism that directly calibrates variance using the Gaussian cumulative density function instead of relying on a tail-bound approximation. Their work is orthogonal to ours and can be incorporated ours as the underlying perturbation mechanism. Lee et al. [[31]](#ref-31) selected the best learning rate from a candidate set based on model evaluation and implemented adaptive privacy budget allocation in each round of DPSGD training. While both our work and theirs involve adaptive DPSGD, there are three significant distinctions. First, their adaptiveness is from adaptive learning rates, which modifies the gradient descent's step size but not its direction. Second, the DP privacy guarantee is different. Ours relies on differences in loss values before and after iterations, whereas theirs adopts NoisyMax[[18]](#ref-18) method on loss values from a variety of models obtained through different learning rates in a single iteration. In contrast, we aim to ensure each gradient descent moves in the desired direction through resampling and re-noising. Third, we do not perform adaptive privacy budget allocation but instead introduce selective release techniques to preserve the privacy budget.Further, Xu et al. [[61]](#ref-61) employed the Root Mean Square Prop (RMSProp) gradient descent technique to adaptively add noise to coordinates of the gradient. Since then, many works [[23]](#ref-23), [[65]](#ref-65), [[71]](#ref-71) have focused on reducing the dimensionality of the model during training to reduce the impact of noise on the overall model.

Poisson sampling. Wei et al. [[57]](#ref-57) first explored the problem of bias due to Poisson sampling in DPSGD and proposed DPIS, which weights the importance sampling by the gradient norm of the sample. Our algorithm mitigates the impact of Poisson sampling on convergence speed through the process of resampling.

Models, pre-processing and parameter tuning. Papernot et al. [[41]](#ref-41) found that using a family of bounded activation functions (tempered sigmoids) instead of the unbounded activation function ReLU in DPSGD can achieve good performance. Tramer et al. [[53]](#ref-53) used Scattering Network to traverse the image in advance to extract features before DPSGD training. Soham et al. [[13]](#ref-13) combined careful hyper-parameter tuning with group normalization and weight standardization to yield remarkable performance benefits. These works are orthogonal to our work.

Privacy accounting. Abadi et al. [[1]](#ref-1) proposed a method called the Moments Accountant (MA) for giving an upper bound the privacy curve of a composition of DPSGD. The Moments Accountant was subsumed into the framework of Renyi Differential Privacy (RDP) introduced by [[36]](#ref-36). Bu et al. [[7]](#ref-7) introduced the notion of Gaussian Differential Privacy (GDP) base hypothesis test. There also exits other variants of DP, for example Concentrated DP (CDP) [[8]](#ref-8) and zero Concentrated-DP [[8]](#ref-8). These variants are tailored for specific scenarios and can be converted into one another under certain conditions. Our primary focus is on (ε, δ)-differential privacy, as it is the most prevalent and widely adopted in both academic literature and practical applications. Besides, many works [[14]](#ref-14), [[15]](#ref-15), [[63]](#ref-63), [[64]](#ref-64), [[69]](#ref-69) based on local differential privacy focus on ε- differential privacy.

### 8 CONCLUSION

We propose DPSUR, a differentially private scheme for deep learning based on selective update and release. Our scheme utilizes the validation test to select appropriate model updates in each iteration, thereby speeding up model convergence and enhancing utility. To reduce the injected Gaussian noise, we incorporate a clipping strategy and a threshold mechanism for gradient selection in each iteration. Furthermore, we apply the Gaussian mechanism with selective release to reduce privacy budget consumption across iterations. We conduct a comprehensive privacy analysis of our approach using RDP and validate our scheme through extensive experiments. The results indicate that DPSUR significantly outperforms state-of-the-art solutions in terms of model utility and downstream tasks. Our scheme is widely applicable to various neural networks, and can serve as a flexible optimizer for new DPSGD variants. For future work, we plan to extend DPSUR to larger models and datasets and theoretically analyze its convergence speed.

### ACKNOWLEDGMENTS

This work was support by the Natural Science Foundation of Shanghai (Grant No. 22ZR1419100), CAAI-Huawei MindSpore Open Fund (Grant No. CAAIXSJLJJ-2022-005A), National Natural Science Foundation of China Key Program (Grant No. 62132005), National Natural Science Foundation of China (Grant No: 92270123 and 62372122), and the Research Grants Council, Hong Kong SAR, China (Grant No: 15209922, 15208923 and 15210023).

## REFERENCES

* <a id="ref-1"></a>[1] Martin Abadi, Andy Chu, Ian Goodfellow, H Brendan McMahan, Ilya Mironov, Kunal Talwar, and Li Zhang. 2016. Deep learning with differential privacy. In Proceedings of the 2016 ACM SIGSAC conference on computer and communications security. 308–318.
* <a id="ref-2"></a>[2] Galen Andrew, Om Thakkar, Brendan McMahan, and Swaroop Ramaswamy. 2021. Differentially private learning with adaptive clipping. Advances in Neural Information Processing Systems 34 (2021), 17455–17466.
* <a id="ref-3"></a>[3] Borja Balle, Gilles Barthe, Marco Gaboardi, Justin Hsu, and Tetsuya Sato. 2020. Hypothesis testing interpretations and renyi differential privacy. In International Conference on Artificial Intelligence and Statistics. PMLR, 2496–2506.
* <a id="ref-4"></a>[4] Borja Balle and Yu-Xiang Wang. 2018. Improving the gaussian mechanism for differential privacy: Analytical calibration and optimal denoising. In International Conference on Machine Learning. PMLR, 394–403.
* <a id="ref-5"></a>[5] Raef Bassily, Adam Smith, and Abhradeep Thakurta. 2014. Private empirical risk minimization: Efficient algorithms and tight error bounds. In 2014 IEEE 55th annual symposium on foundations of computer science. IEEE, 464–473.
* <a id="ref-6"></a>[6] Léon Bottou. 2009. Curiously fast convergence of some stochastic gradient descent algorithms. In Proceedings of the symposium on learning and data science, Paris, Vol. 8. Citeseer, 2624–2633.
* <a id="ref-7"></a>[7] Zhiqi Bu, Jinshuo Dong, Qi Long, and Weijie J Su. 2020. Deep learning with gaussian differential privacy. Harvard data science review 2020, 23 (2020), 10– 1162.
* <a id="ref-8"></a>[8] Mark Bun and Thomas Steinke. 2016. Concentrated Differential Privacy: Simplifications, Extensions, and Lower Bounds. 635–658. [https://doi.org/10.1007/978-3-662-53641-4_24](https://doi.org/10.1007/978-3-662-53641-4_24)
* <a id="ref-9"></a>[9] Nicholas Carlini, Chang Liu, Úlfar Erlingsson, Jernej Kos, and Dawn Song. 2019. The secret sharer: Evaluating and testing unintended memorization in neural networks. In 28th USENIX Security Symposium (USENIX Security 19). 267–284.
* <a id="ref-10"></a>[10] Mia Xu Chen, Benjamin N Lee, Gagan Bansal, Yuan Cao, Shuyuan Zhang, Justin Lu, Jackie Tsay, Yinan Wang, Andrew M Dai, Zhifeng Chen, et al. 2019. Gmail smart compose: Real-time assisted writing. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2287– 2295.
* <a id="ref-11"></a>[11] François Chollet et al. 2015. Keras. [https://keras.io](https://keras.io).
* <a id="ref-12"></a>[12] Rachel Cummings and Deven Desai. 2018. The role of differential privacy in gdpr compliance. In FAT'18: Proceedings of the Conference on Fairness, Accountability, and Transparency. 20.
* <a id="ref-13"></a>[13] Soham De, Leonard Berrada, Jamie Hayes, Samuel L Smith, and Borja Balle. 2022. Unlocking high-accuracy differentially private image classification through scale. arXiv preprint arXiv:2204.13650 (2022).
* <a id="ref-14"></a>[14] Rong Du, Qingqing Ye, Yue Fu, Haibo Hu, Jin Li, Chengfang Fang, and Jie Shi. 2023. Differential Aggregation against General Colluding Attackers. In Proceedings of the IEEE International Conference on Data Engineering.
* <a id="ref-15"></a>[15] Jiawei Duan, Qingqing Ye, and Haibo Hu. 2022. Utility analysis and enhancement of LDP mechanisms in high-dimensional space. In 2022 IEEE 38th International Conference on Data Engineering (ICDE). IEEE, 407–419.
* <a id="ref-16"></a>[16] Cynthia Dwork. 2011. A firm foundation for private data analysis. Commun. ACM 54, 1 (2011), 86–95.
* <a id="ref-17"></a>[17] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006. Calibrating noise to sensitivity in private data analysis. In Theory of Cryptography: Third Theory of Cryptography Conference, TCC 2006, New York, NY, USA, March 4-7, 2006. Proceedings 3. Springer, 265–284.
* <a id="ref-18"></a>[18] Cynthia Dwork and Aaron Roth. 2014. The Algorithmic Foundations of Differential Privacy. TCS 9 (2014), 211–407. Issue 3-4.
* <a id="ref-19"></a>[19] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations of differential privacy. Foundations and Trends® in Theoretical Computer Science 9, 3–4 (2014), 211–407.
* <a id="ref-20"></a>[20] Vitaly Feldman. 2020. Does learning require memorization? a short tale about a long tail. In Proceedings of the 52nd Annual ACM SIGACT Symposium on Theory of Computing. 954–959.
* <a id="ref-21"></a>[21] Matt Fredrikson, Somesh Jha, and Thomas Ristenpart. 2015. Model inversion attacks that exploit confidence information and basic countermeasures. In Proceedings of the 22nd ACM SIGSAC conference on computer and communications security. 1322–1333.
* <a id="ref-22"></a>[22] Rong Ge, Furong Huang, Chi Jin, and Yang Yuan. 2015. Escaping from saddle points—online stochastic gradient for tensor decomposition. In Conference on learning theory. PMLR, 797–842.
* <a id="ref-23"></a>[23] Aditya Golatkar, Alessandro Achille, Yu-Xiang Wang, Aaron Roth, Michael Kearns, and Stefano Soatto. 2022. Mixed differential privacy in computer vision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 8376–8386.
* <a id="ref-24"></a>[24] Mert Gürbüzbalaban, Asu Ozdaglar, and Pablo A Parrilo. 2021. Why random reshuffling beats stochastic gradient descent. Mathematical Programming 186 (2021), 49–84.
* <a id="ref-25"></a>[25] Bargav Jayaraman and David Evans. 2019. Evaluating differentially private machine learning in practice. In 28th USENIX Security Symposium (USENIX Security 19). 1895–1912.
* <a id="ref-26"></a>[26] Angelos Katharopoulos and François Fleuret. 2018. Not all samples are created equal: Deep learning with importance sampling. In International conference on machine learning. PMLR, 2525–2534.
* <a id="ref-27"></a>[27] Scott Kirkpatrick, C Daniel Gelatt Jr, and Mario P Vecchi. 1983. Optimization by simulated annealing. science 220, 4598 (1983), 671–680.
* <a id="ref-28"></a>[28] Antti Koskela and Antti Honkela. 2018. Learning rate adaptation for differentially private stochastic gradient descent.
* <a id="ref-29"></a>[29] A. Krizhevsky and G. Hinton. 2009. Learning multiple layers of features from tiny images. Master's thesis, Department of Computer Science, University of Toronto (2009).
* <a id="ref-30"></a>[30] Yann LeCun, Corinna Cortes, and CJ Burges. 2010. MNIST handwritten digit database. ATT Labs [Online]. Available: http://yann.lecun.com/exdb/mnist 2 (2010).
* <a id="ref-31"></a>[31] Jaewoo Lee and Daniel Kifer. 2018. Concentrated differentially private gradient descent with adaptive per-iteration privacy budget. In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 1656–1665.
* <a id="ref-32"></a>[32] Alexander Selvikvåg Lundervold and Arvid Lundervold. 2019. An overview of deep learning in medical imaging focusing on MRI. Zeitschrift für Medizinische Physik 29, 2 (2019), 102–127.
* <a id="ref-33"></a>[33] Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. 2011. Learning Word Vectors for Sentiment Analysis. In The 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies, Proceedings of the Conference, 19-24 June, 2011, Portland, Oregon, USA. The Association for Computer Linguistics, 142–150.
* <a id="ref-34"></a>[34] Luca Melis, Congzheng Song, Emiliano De Cristofaro, and Vitaly Shmatikov. 2019. Exploiting unintended feature leakage in collaborative learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 691–706.
* <a id="ref-35"></a>[35] Nicholas Metropolis, Arianna W Rosenbluth, Marshall N Rosenbluth, Augusta H Teller, and Edward Teller. 1953. Equation of state calculations by fast computing machines. The journal of chemical physics 21, 6 (1953), 1087–1092.
* <a id="ref-36"></a>[36] Ilya Mironov. 2017. Rényi differential privacy. In 2017 IEEE 30th computer security foundations symposium (CSF). IEEE, 263–275.
* <a id="ref-37"></a>[37] Ilya Mironov, Kunal Talwar, and Li Zhang. 2019. Rényi Differential Privacy of the Sampled Gaussian Mechanism. arXiv: Learning (2019).
* <a id="ref-38"></a>[38] Milad Nasr, Reza Shokri, and Amir Houmansadr. 2019. Comprehensive privacy analysis of deep learning: Passive and active white-box inference attacks against centralized and federated learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 739–753.
* <a id="ref-39"></a>[39] Nicolas Papernot, Martın Abadi, Ulfar Erlingsson, Ian Goodfellow, and Kunal Talwar. 2017. SEMI-SUPERVISED KNOWLEDGE TRANSFER FOR DEEP LEARN-ING FROM PRIVATE TRAINING DATA. stat 1050 (2017), 3.
* <a id="ref-40"></a>[40] Nicolas Papernot, Shuang Song, Ilya Mironov, Ananth Raghunathan, Kunal Talwar, and Úlfar Erlingsson. 2018. Scalable private learning with pate. arXiv preprint arXiv:1802.08908 (2018).
* <a id="ref-41"></a>[41] Nicolas Papernot, Abhradeep Thakurta, Shuang Song, Steve Chien, and Úlfar Erlingsson. 2021. Tempered sigmoid activations for deep learning with differential privacy. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35. 9312–9321.
* <a id="ref-42"></a>[42] NhatHai Phan, Xintao Wu, Han Hu, and Dejing Dou. 2017. Adaptive laplace mechanism: Differential privacy preservation in deep learning. In 2017 IEEE international conference on data mining (ICDM). IEEE, 385–394.
* <a id="ref-43"></a>[43] Le Trieu Phong, Yoshinori Aono, Takuya Hayashi, Lihua Wang, and Shiho Moriai. 2017. Privacy-preserving deep learning: Revisited and enhanced. In Applications and Techniques in Information Security: 8th International Conference, ATIS 2017, Auckland, New Zealand, July 6–7, 2017, Proceedings. Springer, 100–110.
* <a id="ref-44"></a>[44] Venkatadheeraj Pichapati, Ananda Theertha Suresh, Felix X Yu, Sashank J Reddi, and Sanjiv Kumar. 2019. AdaCliP: Adaptive clipping for private SGD. arXiv preprint arXiv:1908.07643 (2019).
* <a id="ref-45"></a>[45] Automatic Differentiation In Pytorch. 2018. Pytorch.
* <a id="ref-46"></a>[46] Ahmed Salem, Yang Zhang, Mathias Humbert, Pascal Berrang, Mario Fritz, and Michael Backes. 2019. ML-Leaks: Model and Data Independent Membership Inference Attacks and Defenses on Machine Learning Models. In Network and Distributed Systems Security (NDSS) Symposium 2019.
* <a id="ref-47"></a>[47] Reza Shokri and Vitaly Shmatikov. 2015. Privacy-preserving deep learning. In Proceedings of the 22nd ACM SIGSAC conference on computer and communications security. 1310–1321.
* <a id="ref-48"></a>[48] Reza Shokri, Marco Stronati, Congzheng Song, and Vitaly Shmatikov. 2017. Membership inference attacks against machine learning models. In 2017 IEEE symposium on security and privacy (SP). IEEE, 3–18.
* <a id="ref-49"></a>[49] Congzheng Song, Thomas Ristenpart, and Vitaly Shmatikov. 2017. Machine learning models that remember too much. (2017), 587–601.
* <a id="ref-50"></a>[50] Shuang Song, Kamalika Chaudhuri, and Anand D Sarwate. 2013. Stochastic gradient descent with differentially private updates. In 2013 IEEE global conference on signal and information processing. IEEE, 245–248.
* <a id="ref-51"></a>[51] Pierre Stock, Igor Shilov, Ilya Mironov, and Alexandre Sablayrolles. 2022. Defending against Reconstruction Attacks with Rényi Differential Privacy. arXiv e-prints (2022), arXiv–2202.
* <a id="ref-52"></a>[52] Kenji Suzuki. 2017. Overview of deep learning in medical imaging. Radiological physics and technology 10, 3 (2017), 257–273.
* <a id="ref-53"></a>[53] Florian Tramer and Dan Boneh. 2020. Differentially Private Learning Needs Better Features (or Much More Data). In International Conference on Learning Representations.
* <a id="ref-54"></a>[54] Tim Van Erven and Peter Harremos. 2014. Rényi divergence and Kullback-Leibler divergence. IEEE Transactions on Information Theory 60, 7 (2014), 3797–3820.
* <a id="ref-55"></a>[55] KoenS.vander Veen, Ruben Seggers, Peter Bloem, and Giorgio Patrini. 2018. Three Tools for Practical Differential Privacy.
* <a id="ref-56"></a>[56] Zhibo Wang, Mengkai Song, Zhifei Zhang, Yang Song, Qian Wang, and Hairong Qi. 2019. Beyond inferring class representatives: User-level privacy leakage from federated learning. In IEEE INFOCOM 2019-IEEE conference on computer communications. IEEE, 2512–2520.
* <a id="ref-57"></a>[57] Jianxin Wei, Ergute Bao, Xiaokui Xiao, and Yin Yang. 2022. Dpis: An enhanced mechanism for differentially private sgd with importance sampling. In Proceedings of the 2022 ACM SIGSAC Conference on Computer and Communications Security. 2885–2899.
* <a id="ref-58"></a>[58] Shaomei Wu, Hermes Pique, and Jeffrey Wieland. 2016. Using artificial intelligence to help blind people 'see'facebook.
* <a id="ref-59"></a>[59] Liyao Xiang, Jingbo Yang, and Baochun Li. 2019. Differentially-private deep learning from an optimization perspective. In IEEE INFOCOM 2019-IEEE Conference on Computer Communications. IEEE, 559–567.
* <a id="ref-60"></a>[60] Han Xiao, Kashif Rasul, and Roland Vollgraf. 2017. Fashion-MNIST: a Novel Image Dataset for Benchmarking Machine Learning Algorithms. arXiv e-prints (2017), arXiv–1708.
* <a id="ref-61"></a>[61] Zhiying Xu, Shuyu Shi, Alex X Liu, Jun Zhao, and Lin Chen. 2020. An adaptive and fast convergent approach to differentially private deep learning. In IEEE INFOCOM 2020-IEEE Conference on Computer Communications. IEEE, 1867–1876.
* <a id="ref-62"></a>[62] Xiaodong Yang, Huishuai Zhang, Wei Chen, and Tie-Yan Liu. 2022. Normalized/clipped sgd with perturbation for differentially private non-convex optimization. arXiv preprint arXiv:2206.13033 (2022).
* <a id="ref-63"></a>[63] Qingqing Ye, Haibo Hu, Kai Huang, Man Ho Au, and Qiao Xue. 2023. Stateful switch: Optimized time series release with local differential privacy. In IEEE INFOCOM 2023-IEEE Conference on Computer Communications. IEEE, 1–10.
* <a id="ref-64"></a>[64] Qingqing Ye, Haibo Hu, Xiaofeng Meng, Huadi Zheng, Kai Huang, Chengfang Fang, and Jie Shi. 2023. PrivKVM*: Revisiting Key-Value Statistics Estimation With Local Differential Privacy. IEEE Transactions on Dependable and Secure Computing (Jan 2023), 17–35.https://doi.org/10.1109/tdsc.2021.3107512
* <a id="ref-65"></a>[65] Da Yu, Huishuai Zhang, Wei Chen, and Tie-Yan Liu. 2020. Do not Let Privacy Overbill Utility: Gradient Embedding Perturbation for Private Learning. In International Conference on Learning Representations.
* <a id="ref-66"></a>[66] Lei Yu, Ling Liu, Calton Pu, Mehmet Emre Gursoy, and Stacey Truex. 2019. Differentially private model publishing for deep learning. In 2019 IEEE symposium on security and privacy (SP). IEEE, 332–349.
* <a id="ref-67"></a>[67] Jianyi Zhang, Yang Zhao, and Changyou Chen. 2020. Variance reduction in stochastic particle-optimization sampling. In International Conference on Machine Learning. PMLR, 11307–11316.
* <a id="ref-68"></a>[68] Xinyang Zhang, Shouling Ji, and Ting Wang. 2018. Differentially Private Releasing via Deep Generative Model (Technical Report). arXiv e-prints (2018), arXiv–1801.
* <a id="ref-69"></a>[69] Yuemin Zhang, Qingqing Ye, Rui Chen, Haibo Hu, and Qilong Han. 2023. Trajectory Data Collection with Local Differential Privacy. Proceedings of the VLDB Endowment 16, 10 (2023), 2591–2604.
* <a id="ref-70"></a>[70] S Kevin Zhou, Hayit Greenspan, Christos Davatzikos, James S Duncan, Bram Van Ginneken, Anant Madabhushi, Jerry L Prince, Daniel Rueckert, and Ronald M Summers. 2021. A review of deep learning in medical imaging: Imaging traits, technology trends, case studies with progress highlights, and future promises. Proc. IEEE 109, 5 (2021), 820–838.
* <a id="ref-71"></a>[71] Yingxue Zhou, Steven Wu, and Arindam Banerjee. 2020. Bypassing the Ambient Dimension: Private SGD with Gradient Subspace Identification. In International Conference on Learning Representations.
* <a id="ref-72"></a>[72] Ligeng Zhu, Zhijian Liu, and Song Han. 2019. Deep leakage from gradients. Advances in Neural Information Processing Systems 32 (2019).
* <a id="ref-73"></a>[73] Tianqing Zhu, Gang Li, Wanlei Zhou, and S Yu Philip. 2017. Differential Privacy and Applications. Vol. 69. Springer.

## A RDP OF TWO TRUNCATED NORMAL DISTRIBUTIONS

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)||f(x; 0, \mu\sigma, a, b))
$$

$$
\frac{1}{\alpha-1} \cdot \log \int_{a}^{b} \frac{[f(x;\mu,\mu\sigma,a,b)]^{\alpha}}{[f(x;\mu,\mu\sigma,a,b)]^{\alpha-1}} dx
$$

$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \int_{a}^{b} \frac{1}{\mu\sigma\sqrt{2\pi}}
$$

$$
\cdot \exp\left(-\frac{\alpha(x-\mu)^{2}}{2\mu^{2}\sigma^{2}}\right) \cdot \exp\left(-\frac{(1-\alpha)x^{2}}{2\mu^{2}\sigma^{2}}\right) dx\}
$$

$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma\sqrt{2\pi}} \int_{a}^{b} \exp\left[(-x^{2}+\frac{(2\mu^{2}\sigma^{2})}{2\sigma^{2}})\right] dx\}
$$

$$
= \frac{1}{\alpha-1} \cdot \log \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \int_{a}^{b} \exp\left(\frac{\alpha(\alpha-1)}{2\sigma^{2}}\right) dx\}
$$

$$
= \frac{1}{\alpha-1} \cdot \left\{\frac{\alpha(\alpha-1)}{2\sigma^{2}} + \log\left[\frac{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha-1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \right\}
$$

$$
\int_{a}^{b} \exp\left(-\left(\frac{x-\alpha\mu}{\sqrt{2\mu\sigma}}\right)^{2}\right) d\left(\frac{x-\alpha\mu}{\sqrt{2\mu\sigma}}\right)\right] dx
$$

**Table 5:** MNIST and FMNIST model architecture

| Layer | Parameters |
|---|---|
| Convolution | 16 filters of 8×8, stride 2,padding 2 |
| Max-Pooling | 2×2, stride 1 |
| Convolution | 32 filters of 4×4, stride 2, padding 0 |
| Max-Pooling | 2×2, stride 1 |
| Fully connected | 32 units |
| Fully connected | 10 units |

### Table 6: CIFAR-10 model architecture

| Layer | Parameters |
|---|---|
| Convolution×2 | 32 filters of 3×3, stride 1, padding 1 |
| Max-Pooling | 2×2, stride 2 |
| Convolution×2 | 64 filters of 3×3, stride 1, padding 1 |
| Max-Pooling | 2×2, stride 2 |
| Convolution×2 | 128 filters of 3×3, stride 1, padding 1 |
| Max-Pooling | 2×2, stride 2 |
| Fully connected | 128 units |
| Fully connected | 10 units |

### Table 7: IMDb model architecture.

| Layer | Parameters |
|---|---|
| Embedding | 100 units |
| Fully connected | 32 units |
| Bidirectional LSTM | 32 units |
| Fully connected | 16 units |
| Fully connected | 2 units |

$$
D_{\alpha}(f(x; \mu, \mu\sigma, a, b)) |f(x; 0, \mu\sigma, a, b))
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \int_{a}^{b} \frac{[f(x; \mu, \mu\sigma, a, b)]^{\alpha}}{[f(x; 0, \mu\sigma, a, b)]^{\alpha - 1}} dx
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \int_{a}^{b} \frac{1}{\mu\sigma \sqrt{2\pi}}
$$

$$
\cdot \exp(-\frac{\alpha(x - \mu)^{2}}{2\mu^{2}\sigma^{2}}) \cdot \exp(-\frac{(-1 - \alpha)x^{2}}{2\mu^{2}\sigma^{2}}) dx\}
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\mu\sigma \sqrt{2\pi}} \int_{a}^{b} \exp\left[(-x^{2} + 2a\mu x - \alpha\mu^{2}) / (2\mu^{2}\sigma^{2})\right] dx\}
$$

$$
= \frac{1}{\alpha - 1} \cdot \ln \{\frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}} \int_{a}^{b} exp(\frac{\alpha(\alpha - 1)}{2\sigma^{2}}) dx\}
$$

$$
= \frac{1}{\alpha - 1} \cdot \{\frac{\alpha(\alpha - 1)}{\alpha^{2}\mu\sigma} + \ln \frac{(\Phi(\frac{b}{\mu\sigma}) - \Phi(\frac{a}{\mu\sigma}))^{\alpha - 1}}{(\Phi(\frac{b-\mu}{\mu\sigma}) - \Phi(\frac{a-\mu}{\mu\sigma}))^{\alpha}} \cdot \frac{1}{\sqrt{\pi}}
$$

$$
\int_{a}^{b} exp(-\frac{x - \alpha\mu}{\sqrt{2\mu\sigma}}) dx
$$

### B MODEL ARCHITECTURES