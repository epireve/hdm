---
cite_key: "arxiv_220315696_auditing_priva"
title: "Auditing Privacy Defenses in Federated Learning via Generative Gradient Leakage"
year: 2012
date_processed: "2025-07-02"
phase2_processed: true
original_folder: "arxiv_2203.15696_Auditing_Privacy_Defenses_in_Federated_Learning_vi"
images_total: 15
images_kept: 15
images_removed: 0
---

# Auditing Privacy Defenses in Federated Learning via Generative Gradient Leakage

<span id="page-0-2"></span>Zhuohang Li<sup>1</sup> Jiaxin Zhang<sup>2</sup> Luyang Liu<sup>3</sup> Jian Liu<sup>1</sup> <sup>1</sup>University of Tennessee, Knoxville <sup>2</sup>Oak Ridge National Laboratory <sup>3</sup>Google Research zli96@vols.utk.edu, zhangj@ornl.gov, luyangliu@google.com, jliu@utk.edu

# Abstract

*Federated Learning (FL) framework brings privacy benefits to distributed learning systems by allowing multiple clients to participate in a learning task under the coordination of a central server without exchanging their private data. However, recent studies have revealed that private information can still be leaked through shared gradient information. To further protect user's privacy, several defense mechanisms have been proposed to prevent privacy leakage via gradient information degradation methods, such as using additive noise or gradient compression before sharing it with the server. In this work, we validate that the private training data can still be leaked under certain defense settings with a new type of leakage, i.e., Generative Gradient Leakage (GGL). Unlike existing methods that only rely on gradient information to reconstruct data, our method leverages the latent space of generative adversarial networks (GAN) learned from public image datasets as a prior to compensate for the informational loss during gradient degradation. To address the nonlinearity caused by the gradient operator and the GAN model, we explore various gradient-free optimization methods (e.g., evolution strategies and Bayesian optimization) and empirically show their superiority in reconstructing high-quality images from gradients compared to gradient-based optimizers. We hope the proposed method can serve as a tool for empirically measuring the amount of privacy leakage to facilitate the design of more robust defense mechanisms*[1](#page-0-0) *.*# Introduction

Federated Learning (FL) [\[26,](#page-9-0) [29,](#page-9-1) [34\]](#page-9-2) has recently emerged as a new machine learning paradigm that enables multiple clients to collaboratively train a global learning model under the orchestration of a central server. Instead of directly exchanging their private data, each client learns

<span id="page-0-1"></span>![](_page_0_Figure_7.jpeg)

Figure 1. Illustration of data leakage via gradient: 1 Client computes gradients on its private data; 2 Client applies defense to degrade the computed gradients y; 3 Adversary attempts to reconstruct the private image from the shared gradients y 0 .

on its local dataset and shares the computed model update or gradient to update the global model. FL places a heavy emphasis on user's data privacy, which has made it particularly suitable for developing machine learning models in privacysensitive scenarios such as typing prediction [\[21\]](#page-9-3), spoken language understanding [\[16,](#page-9-4)[20\]](#page-9-5), medical research [\[4,](#page-8-0)[8,](#page-8-1)[41\]](#page-10-0), and financial services [\[32,](#page-9-6) [50\]](#page-10-1).

Although FL is designed to structurally encode data minimization principles to protect privacy, recent studies have revealed that, in certain cases, sensitive information can still be leaked through the shared gradients [\[13,](#page-9-7) [35,](#page-9-8) [51,](#page-10-2) [54,](#page-10-3) [56\]](#page-10-4). To further strengthen FL's privacy properties in these cases, several defense strategies have been proposed to*degrade*the gradient information before sharing it with the server, such as differential privacy [\[14,](#page-9-9) [48\]](#page-10-5), gradient compression/sparsification [\[56\]](#page-10-4), and perturbing gradients via data representations [\[44\]](#page-10-6). These state-of-the-art privacy defenses have been shown to be effective against existing attacks through modifying the gradient information to degrade its fidelity prior to sharing.

<span id="page-0-0"></span><sup>1</sup>Code is available at: [https://github.com/zhuohangli/](https://github.com/zhuohangli/GGL) [GGL](https://github.com/zhuohangli/GGL)

<span id="page-1-0"></span>A natural question is:*Can the aforementioned defenses provide sufficient privacy guarantees to prevent the leakage of sensitive information from the client's private data?*To investigate this, we model the gradient leakage process as an inverse problem, where the goal is to reconstruct the private training data from the client's shared low-fidelity and noisy gradients. Existing methods seek to solve this inverse problem by iteratively solving for the optimal set of data samples that best match the client's shared gradients via an optimization process (e.g., gradient descent [\[13,](#page-9-7) [51\]](#page-10-2) or L-BFGS [\[54,](#page-10-3) [56\]](#page-10-4)). However, such a problem is ill-posed as there are infinite sets of feasible solutions in the image space and the outcome of the reconstruction may not be a decent natural image. To solve this, existing attacks [\[13,](#page-9-7) [51\]](#page-10-2) utilize handcrafted image priors such as total variation [\[33\]](#page-9-10) to regularize the reconstruction process. Although such prior constraint is relatively effective when there is no defense, we find that it is still not sufficiently tight (i.e., many nonimage signals can satisfy this constraint) for reconstructing from low-fidelity and noisy gradient observations, causing existing attacks to falsely return unrealistic images when a defense mechanism is applied (e.g., differential privacy), as illustrated in Figure [1.](#page-0-1)

In this work, we demonstrate on two image datasets that recovering high-fidelity images from shared gradients is still feasible even under certain defense settings by introducing a new type of leakage, namely Generative Gradient Leakage (GGL). As shown in Figure [1,](#page-0-1) our method leverages the manifold of the generative adversarial network (GAN) [\[6,](#page-8-2)[15,](#page-9-11)[27\]](#page-9-12) learned from a large public image dataset as prior information, which provides a good proximation of the natural image space. By minimizing the gradient matching loss in the GAN image manifold, our method can find images that are highly similar to the client's private training data with high quality. However, solving such an optimization problem is not trivial as both the gradient operator and the GAN latent space are highly non-linear and non-convex, and the defense methods applied at the client's side also inject noises into the objective function. To resolve this, we design an adaptive loss function against common defenses by considering the underlying gradient transformation and resort to gradient-free optimization methods (e.g., evolution strategies [\[19\]](#page-9-13) and Bayesian optimization [\[10\]](#page-8-3)) to search for the global minima within the GAN latent space. We empirically demonstrate that compared with gradient-based optimizers, doing so significantly reduces the chance of converging to a local minimum, leading to a higher quality of reconstructed images as well as improved similarity to the client's private image. We note that the findings made from the chosen defense settings and datasets may not be general in scope. Nevertheless, we expect the proposed method can serve as a means for privacy auditing in FL by showing how much an adversary can learn under a specific defense setting to assist the future design of privacy mechanisms. Our main contributions are summarized as follows:

- We propose to solve the inverse problem of gradient leakage in FL under noises and defensive transformations by leveraging the prior information learned from deep generative models.
- We systematically study 4 types of gradient-degradationbased defenses, including additive noise, gradient clipping, gradient compression, and representation perturbation, and design adaptive loss functions by accounting for the underlying gradient transformation.
- To avoid sub-optimal solutions and reveal more private information, we compare different gradient-free optimizers with conventional gradient-based optimizers (e.g., Adam) and experimentally show their superiority for gradient leakage attack in terms of reconstructed image quality and its similarity to the client's private image.
- We demonstrate on two image datasets (i.e., CelebA [\[31\]](#page-9-14) and ImageNet [\[9\]](#page-8-4)) that with the proposed GGL, highresolution images can still be recovered from the shared gradients even with the considered defenses, while existing gradient leakage attacks all fail.

# Related Work

## 1. Privacy Leakage via Gradient

The studies on privacy leakage in FL originate from*membership inference*, where a malicious analyst infers whether a specific data sample has been involved in the training set [\[38\]](#page-9-15). Moreover, researchers have discovered that the exchanged model updates can be utilized to further infer unintended private information, such as the retrieval of certain *input attributes*[\[11,](#page-8-5) [35\]](#page-9-8) (e.g., whether people in the training data wear glasses). Further studies find it is possible to recover class-level [\[24\]](#page-9-16) or even client-level*data representatives*[\[47\]](#page-10-7) (i.e., prototypical samples of the private training set) through generative modeling.

Data Reconstruction Attacks. Recently, Zhu *et al.*[\[56\]](#page-10-4) demonstrate a more severe type of privacy threat where an attacker can fully restore the client's private data samples by solving for the optimal pair of input and label that best matches the exchanged gradients. A follow-up work [\[54\]](#page-10-3) improves on this method by proposing a method for analytically extracting the label information. However, these methods are limited to shallow networks trained with lowresolution images. A later study by Geiping*et al.*[\[13\]](#page-9-7) extends this attack to more realistic scenarios by successfully restoring ImageNet-level high-resolution data from deeper networks (e.g, ResNet [\[23\]](#page-9-17)) using a magnitude-invariant loss design. Along this direction, a more recent work by Yin*et al.*[\[51\]](#page-10-2) even achieves image batch reconstruction by utilizing the strong prior encoded in batch normalization <span id="page-2-2"></span>statistics. Despite the improvement, the current research efforts on data reconstruction attacks often assume an ideal setting by targeting a bare-bone FL system without applying any additional privacy-preserving measures or defenses, which contradicts industrial practices.

## 2. Privacy Preservation in FL

Existing research efforts for achieving privacy preservation in FL can be generally categorized into*cryptographybased*and*gradient-degradation-based*approaches.

A common type of cryptographic solution is secure multi-party computation (MPC), which aims to have a set of parties to jointly compute the output of a function over their private inputs in a way that only the intended output is revealed to the parties. This can be achieved by designing custom protocols [\[1,](#page-8-6) [37\]](#page-9-18), or via secure aggregation schemes such as homomorphic encryption [\[22\]](#page-9-19) and secret sharing [\[49\]](#page-10-8). However, merely relying on MPC isn't sufficient to resist inference attacks over the output [\[35,](#page-9-8) [45\]](#page-10-9).

Another line of research seeks to constrain the amount of leaked sensitive information by intentionally sharing degraded gradients. Differential privacy (DP) is the standard way to quantify and limit the privacy disclosure about individual users. DP can be applied at either the server's side (central DP) or the client's side (local DP). In comparison, local DP provides a better notion of privacy as it does not require the client to trust anyone. It utilizes a randomized mechanism to distort the gradients before sharing them with the server [\[14,](#page-9-9) [48\]](#page-10-5). DP offers a worst-case information theoretic guarantee on how much an adversary can learn from the released data. However, for these worst-case bounds to be most meaningful, they typically involve adding too much noise which often reduces the utility of the trained models. In addition to DP, it is demonstrated that performing gradient compression/sparsification can also help to prevent information leakage from the gradients [\[56\]](#page-10-4). A most recent work by Sun*et al.* [\[44\]](#page-10-6) identifies the data representation leakage from gradients as the root cause of privacy leakage in FL and proposes a defense named Soteria, which computes the gradients based on perturbed data representations. It is shown that Soteria can achieve a certifiable level of robustness while maintaining good model utility.

# Methodology

## 1. Threat Model

In most existing data leakage attacks [\[13,](#page-9-7) [51,](#page-10-2) [54,](#page-10-3) [56\]](#page-10-4), the adversary is considered to be an honest-but-curious server and has access to the current FL model as well as the shared gradients. As illustrated in Figure [2a,](#page-2-0) we further assume that clients apply a privacy defense locally on the gradients computed from their private data, and the adversary can only access the degraded gradients modified by the defense

<span id="page-2-0"></span>![](_page_2_Figure_8.jpeg)

Figure 2. Illustration of the threat model and the proposed method.

mechanism. The adversary's objective is to reveal as much private information as possible from the degraded gradients. The adversary may or may not know the underlying defense strategy adopted by the client. In either case, the adversary could attempt to launch an adaptive attack by directly using this knowledge or by estimating the defense parameters through the observed gradients. Additionally, we assume the adversary can utilize the knowledge extracted from publicly available datasets (disjoint from client's private data) to facilitate and improve the attack.

## 2. Background

Problem Formulation. The task of reconstructing a training image x ∈ R d from its gradients y ∈ R <sup>m</sup> can be formulated as a non-linear inverse problem:

<span id="page-2-1"></span>
$$
y = F(x), \tag{1}
$$

where F(x) = ∇θL(fθ(x), c) is the forward operator that calculates the gradients of the loss L provided with x and its label c, along with the FL model f<sup>θ</sup> parameterized by θ. When defense is applied at the client's side, the reconstructing problem defined in Equation [1](#page-2-1) becomes:

$$
y = \mathcal{T}(F(x)) + \varepsilon,\tag{2}
$$

where T (·) is referred to as the lossy transformation (e.g., compression or sparsification) and ε means the additive noise (e.g., DP) introduced by the defense algorithm.

Current Approach and Its Limitation. Existing methods [\[13,](#page-9-7) [51,](#page-10-2) [56\]](#page-10-4) aim to solve this inverse problem by using image priors in a penalty form:

$$
\mathbf{x}^* = \operatorname*{argmin}_{\mathbf{x} \in \mathbb{R}^d} \mathcal{D}(\mathbf{y}, F(\mathbf{x})) + \lambda \omega(\mathbf{x}),\tag{3}
$$

where D(·) is a distance metric, ω(x) : R <sup>d</sup> → R is the standard image prior (e.g., total variance [\[2\]](#page-8-7) regularization) and λ is the weight factor. This form has been demonstrated effective for reconstructing images from the actual gradients. However, when reconstructing from a set of low-fidelity and <span id="page-3-1"></span>noisy gradients, such methods would suffer from the limited identification ability of hand-crafted priors, rendering them to return false solutions that are not valid natural images, which is illustrated in Section [4.4.](#page-5-0)

## 3. Generative Gradient Leakage

Motivated by the success of deep generative models for compressed sensing [\[3,](#page-8-8)[46\]](#page-10-10), in this work, we aim to leverage a generative model trained on public datasets as the learned natural image prior to ensure the reconstructed image quality. Moreover, to further account for the privacy defenses that produce degraded gradient information, we propose an adaptive attack by estimating the transformation T (·) and incorporating it in the optimization process. Specifically, given a well-trained generator G(·), we target to solve the following optimization problem:

<span id="page-3-0"></span>
$$
\mathbf{z}^*= \underset{\mathbf{z} \in \mathbb{R}^k}{\operatorname{argmin}} \underbrace{\mathcal{D}\big(\mathbf{y}, \mathcal{T}\big(F(G(\mathbf{z}))\big)\big)}_{\text{gradient matching loss}} + \lambda \underbrace{\mathcal{R}(G; \mathbf{z})}_{\text{regularization}}, \qquad (4)
$$

where z ∈ R k is the latent space of the generative model, R(G; z) is a regularization term that penalizes latent vectors which deviate from the prior distribution, and λ is the weight factor. Once the optimal solution z ∗ is obtained, the image can be reconstructed by G(z ∗ ). An overview of the proposed method is provided in Figure [2b.](#page-2-0) We next describe each component in detail.

Label Inference. Given the shared gradients, the adversary can first adopt an analytical method [\[54\]](#page-10-3) to infer the ground truth label c associated with the client's private image x. Specifically, for FL models performing classification task over n classes, the i th entry of the gradients with respect to the weights of the final fully-connected (FC) classification layer (denoted as ∇W<sup>i</sup> F C ) is given by:

$$
\nabla \mathbf{W}_{FC}^{i} = \frac{\partial \mathcal{L}(f_{\theta}(\mathbf{x}), \mathbf{c})}{\partial z_{i}} \times \frac{\partial z_{i}}{\partial \mathbf{W}_{FC}^{i}},
$$
 (5)

where z<sup>i</sup> is the i th output of the FC layer. Note that computing the second term ∂z<sup>i</sup> ∂W<sup>i</sup> F C results in the post-activation outputs of the previous layer, which will be always nonnegative if activation functions like ReLU or sigmoid are applied. For networks trained with cross-entropy loss on one-hot labels (assuming softmax is applied at the last layer), the first term will be negative if and only if i = c. Thus the ground truth label can be retrieved by identifying the index of the negative entry of ∇W<sup>i</sup> F C . The inferred label will be used for evaluating the FL model training loss L(fθ(x), c). For conditional GANs [\[36\]](#page-9-20), the inferred label will also be used as the class condition.

Gradient Transformation Estimation. The adversary can further attempt to mitigate the impact of the defense by adopting a similar transformation when evaluating the loss of reconstructed images. Although the transformation process at the client's side isn't directly known to the adversary, the adversary can estimate the parameters of the transformation through the observed gradients. Specifically, we consider the following defensive transformations (i.e., T (·)):

(1)*Gradient Clipping*: A common technique used in DP studies [\[14,](#page-9-9) [48\]](#page-10-5) to restrict the contribution of each individual client. Given a clipping bound S, gradient clipping transforms the gradients as Tcli(y, S) = y/max(1, kyk<sup>2</sup> S ). In practice, gradient clipping is often done in a layer-wise manner. The adversary can take the `<sup>2</sup> norm at each layer of the observed gradients as the estimated clipping bound.

(2) *Gradient Sparsification*: Originally proposed for reducing the communication bandwidth of distributed training [\[30\]](#page-9-21), gradient sparsification is also reported to be effective for defending against gradient leakage attacks [\[56\]](#page-10-4). Specifically, given a pruning rate p ∈ (0, 1), the client first computes a threshold τ ← p of |y|, which is then used to produce a mask M ← |y| > τ . Finally, the mask is applied to the gradients during the transformation, i.e., Tspa(y, p) = y  M. This operation is also layer-wise. The adversary can use the percentage of non-zero entries in the observed gradient to estimate its sparsity.

(3) *Representation Perturbation*: The core of the recently proposed Soteria [\[44\]](#page-10-6) defense is to prevent data leakage by perturbing the representation learned from a single fully-connected layer L (i.e., the defended layer) to cause maximal reconstruction error. Assume f<sup>r</sup> : R <sup>d</sup> → R l is the feature extractor before the defended layer that maps x ∈ R d to a l-dimensional data representation r ∈ R l . Specifically, the client first evaluates the impact of each entry of the representation by computing <sup>r</sup>i(∇xfr(ri))<sup>−</sup><sup>1</sup> 2 : i ∈ {0, 1, ..., l − 1} . Given a pruning rate p ∈ (0, 1), the client then prunes the p × l elements in r with the largest <sup>r</sup>i(∇xfr(ri))<sup>−</sup><sup>1</sup> 2 values to get r 0 . Finally, the client computes the gradients on the perturbed representation r 0 . This can be thought as applying a mask only to the gradients of the defended layer: Trep(y, p) = y  ML. As this process is deterministic for a given x and FL model fθ, the adversary can reverse-engineer this mask according to the non-zero entries of the gradients from the defended layer.

Gradient Matching Loss. The first term in the objective function (Equation [4\)](#page-3-0) encourages the solver to find images that are contextually similar to the client's private training images in the generator's latent space by minimizing the distance between the transformed gradients of the generated images ˜y and the observed gradients y. We explore the following distance metrics for calculating the gradient matching loss: (1) *Squared*`<sup>2</sup>*norm*[\[51,](#page-10-2) [54,](#page-10-3) [56\]](#page-10-4): D1(y, ˜y) = ky − ˜yk 2 2 ; and (2)*Cosine Distance*[\[13\]](#page-9-7): D2(y, ˜y) = 1 − <y,˜y> kyk<sup>2</sup> k˜yk<sup>2</sup> . Cosine distance is magnitudeinvariant and is equivalent to optimizing the Euclidean distance of two normalized gradient vectors.

<span id="page-4-3"></span><span id="page-4-0"></span>

| Grad. |               | D1             | D2             |                |  |  |  |
|-------|---------------|----------------|----------------|----------------|--|--|--|
| Reg.  | MSE-I ↓       | PSNR ↑         | MSE-I ↓        | PSNR ↑         |  |  |  |
| R1    | 0.0320±0.0173 | 15.6814±2.6387 | 0.03671±0.0227 | 15.3471±3.1093 |  |  |  |
| R2    | 0.0337±0.0206 | 15.5405±2.7090 | 0.06290±0.0815 | 14.3249±4.1627 |  |  |  |

Table 1. Comparison of different loss function configurations.

Regularization Term. Optimizing with gradient matching loss alone is likely to produce latent vectors that deviate from the generator's latent distribution, resulting in unrealistic images with significant artifacts. To avoid this issue, we explore the following loss functions to regularize the latent vector during the optimization process: (1)*KL-based regularization*[\[28\]](#page-9-22): R1(G; z) = − 1 2 P<sup>k</sup> <sup>i</sup>=1 1 + log σ 2 i − µ 2 <sup>i</sup> − σ 2 i , where µ<sup>i</sup> and σ<sup>i</sup> denote the element-wise mean and standard deviation. The KL term aims to reduce the Kullback–Leibler divergence (KLD) between the latent distribution and the standard Gaussian distribution N (0, I); and (2)*Norm-based regularization*[\[7\]](#page-8-9): R2(G; z) = (kzk 2 <sup>2</sup> − k) 2 , which penalizes latent vectors that are far from the prior distribution.

Optimization Strategy. The target inverse problem described in Equation [4](#page-3-0) is highly non-linear and nonconvex, and thus choosing the right optimization strategy becomes a critical factor for achieving good image reconstruction. Existing data reconstruction attacks are all based on gradient-based optimizers such as L-BFGS [\[54,](#page-10-3) [56\]](#page-10-4) and Adam [\[13,](#page-9-7) [51\]](#page-10-2). The outcome of such local optimization strategies highly depends on the choice of initialization and often requires multiple trials to find a decent solution. Moreover, we find that for more complex generative models, gradient-based optimizers are likely to converge to local minima, leading to poor reconstruction results. Inspired by Huh*et al.*[\[25\]](#page-9-23), besides gradient-based optimizers, we further explore two gradient-free optimization strategies to overcome these issues:

(1)*Bayesian Optimization (BO)*[\[43\]](#page-10-11): BO is a global optimization method that can well handle stochastic noise in blackbox functions, which are modeled by a Gaussian process. Vanilla BO scales poorly to high-dimensional problems [\[43\]](#page-10-11) and thus we adopt a variant of BO, namely, trust region BO (TuRBO) [\[10\]](#page-8-3), for performing a global search in the high-dimensional latent space of the GAN model.

(2)*Covariance Matrix Adaptation Evolution Strategy (CMA-ES)*[\[19\]](#page-9-13): CMA-ES leverages a multivariate normal sampling distribution over the search space. At each step, a stochastic search is performed by drawing samples from that distribution to compute the loss. Evolutionary strategies such as recombination and mutation are used to adaptively update its mean and covariance matrix [\[18\]](#page-9-24).

<span id="page-4-2"></span>![](_page_4_Figure_6.jpeg)

Figure 3. Visual comparison of different optimizers. The images on the right are the reconstruction samples produced by three types of optimizers with different random seeds.

<span id="page-4-1"></span>

|          | Metric         |                | Adam   | BO      |        | CMA-ES  |        |  |
|----------|----------------|----------------|--------|---------|--------|---------|--------|--|
| Dataset  |                | Mean           | Std.   | Mean    | Std.   | Mean    | Std.   |  |
|          | MSE-I ↓ 0.0427 |                | 0.0025 | 0.0813  | 0.0131 | 0.0708  | 0.0008 |  |
| CelebA   |                | PSNR ↑ 13.6965 | 0.2593 | 10.9455 | 0.6816 | 11.4989 | 0.0533 |  |
|          | LPIPS ↓ 0.1435 |                | 0.0083 | 0.2162  | 0.0328 | 0.2136  | 0.0133 |  |
|          | MSE-R ↓ 0.0003 |                | 0.0001 | 0.0012  | 0.0003 | 0.0015  | 0.0022 |  |
| ImageNet | MSE-I ↓ 0.5918 |                | 0.1955 | 0.2648  | 0.0181 | 0.2667  | 0.0119 |  |
|          | PSNR ↑ 2.4433  |                | 1.3565 | 5.7783  | 0.2992 | 5.7420  | 0.1988 |  |
|          | LPIPS ↓ 0.7983 |                | 0.0280 | 0.6166  | 0.0590 | 0.5736  | 0.0209 |  |
|          | MSE-R ↓ 0.1051 |                | 0.0703 | 0.0035  | 0.0005 | 0.0018  | 0.0002 |  |

Table 2. Quantitative comparison of different optimizers.

# Experiments

## 1. Experimental Setup

FL Tasks & Datasets. We evaluate our method on two FL tasks: (1)*Gender Classification*: Binary gender classification performed on the CelebFaces attributes dataset (CelebA) [\[31\]](#page-9-14) with images of size 32 × 32; and (2) *Image Classification*: 1000-class image classification on the ImageNet ILSVRC 2012 dataset [\[9\]](#page-8-4) with images of size 224 × 224. The FL model for all tasks adopts the ResNet-18 [\[23\]](#page-9-17) architecture with randomly initialized weights. We consider the case where the client performs one local step with batch size =1 to compute the gradients.

Implementation. For CelebA dataset, we use the training set containing 162k images to train a DCGAN [\[40\]](#page-9-25) on the Wasserstein loss with gradient penalty [\[17\]](#page-9-26), while the rest images are reserved for evaluation. For experiments on ImageNet dataset, we use a pretrained BigGAN [\[6\]](#page-8-2) released by the authors [\[5\]](#page-8-10). Note that the FL task is performed on the evaluation set which is disjoint from the GAN training set. We use the gradients computed from the FL model after applying defenses to conduct reconstruction.

Evaluation Metrics. Besides qualitative visual comparison, we use the following metrics for quantitative evaluation of the similarity between the target image and the reconstructed image: (1) *Mean Square Error - Image Space (MSE-I* ↓*)*: the pixel-wise MSE between the target image and the reconstructed image; (2) *Peak Signal-to-Noise Ra-*Table 3. Quantitative comparison of GGL with state-of-the-art methods under various defenses.

<span id="page-5-2"></span><span id="page-5-1"></span>

| Attack   |                  | Additive Noise [44, 56] |         |         | Gradient Clipping [14, 48] |                 |         | Gradient Sparsification [56] |               |                 |         | Soteria [44] |        |                 |         |         |         |
|----------|------------------|-------------------------|---------|---------|----------------------------|-----------------|---------|------------------------------|---------------|-----------------|---------|--------------|--------|-----------------|---------|---------|---------|
| Dataset  |                  | MSE-I ↓                 | PSNR ↑  | LPIPS ↓ |                            | MSE-R ↓ MSE-I ↓ | PSNR ↑  | LPIPS ↓                      |               | MSE-R ↓ MSE-I ↓ | PSNR ↑  | LPIPS ↓      |        | MSE-R ↓ MSE-I ↓ | PSNR ↑  | LPIPS ↓ | MSE-R ↓ |
|          | DLG [56] 0.6479  |                         | 1.8843  | 0.8197  | 0.0021                     | 0.2097          | 6.7831  | 0.7375                       | 0.0326        | 0.3335          | 4.7679  | 0.7986       | 0.0155 | 0.3624          | 4.4069  | 0.8007  | 0.0285  |
|          | iDLG [54] 0.6261 |                         | 2.0329  | 0.8209  | 0.0025                     | 0.1960          | 7.0762  | 0.7280                       | 0.0326        | 0.3301          | 4.8124  | 0.8035       | 0.0162 | 0.3269          | 4.8553  | 0.8036  | 0.0396  |
| CelebA   | IG [13]          | 0.4880                  | 3.1151  | 0.8260  | 0.0097 0.0543              |                 | 12.6517 | 0.2998                       | 0.0003 0.4103 |                 | 3.8687  | 0.7975       | 0.0113 | 0.3441          | 4.6326  | 0.8008  | 0.0316  |
|          | GI [51]          | 0.5738                  | 2.4116  | 0.8302  | 0.0023                     | 0.1790          | 7.4701  | 0.7142                       | 0.0322        | 0.2958          | 5.2888  | 0.7775       | 0.0163 | 0.3179          | 4.9768  | 0.7991  | 0.0409  |
|          | GGL              | 0.0780                  | 11.0766 | 0.1906  | 0.0010 0.0760              |                 | 11.1902 | 0.1670                       | 0.0015 0.0768 |                 | 11.1466 | 0.1620       | 0.0007 | 0.0968          | 10.1434 | 0.2561  | 0.0007  |
|          | DLG [56] 0.7438  |                         | 1.2852  | 0.9353  | 0.0049                     | 0.3809          | 4.1912  | 0.9798                       | 2.1610        | 0.4432          | 3.5336  | 0.8907       | 0.0075 | 0.5990          | 2.2253  | 0.9195  | 0.5415  |
|          | iDLG [54] 0.7352 |                         | 1.3359  | 0.9392  | 0.0041                     | 0.3699          | 4.3190  | 0.9473                       | 1.8810        | 0.4357          | 3.6077  | 0.8935       | 0.0077 | 0.6089          | 2.1542  | 0.9198  | 0.5425  |
| ImageNet | IG [13]          | 0.3081                  | 5.1120  | 0.8677  | 0.4490 0.1432              |                 | 8.4386  | 0.7476                       | 0.0214        | 0.2993          | 5.2376  | 0.8805       | 0.0501 | 0.3683          | 4.3373  | 0.8700  | 0.5057  |
|          | GI [51]          | 0.6593                  | 1.8090  | 0.9448  | 0.0031                     | 0.3702          | 4.3154  | 0.9451                       | 1.8807        | 0.4404          | 3.5611  | 0.8889       | 0.0072 | 0.6235          | 2.0511  | 0.9169  | 0.5792  |
|          | GGL              | 0.2686                  | 5.7089  | 0.5915  | 0.0018 0.2230              |                 | 6.5163  | 0.5592                       | 0.0015        | 0.2141          | 6.6920  | 0.5170       | 0.0017 | 0.2484          | 6.0477  | 0.5685  | 0.0022  |
*tio (PSNR* ↑*)*: The ratio of the maximum squared pixel fluctuation and the MSE between the target image and the reconstructed image; (3) *Learned Perceptual Image Patch Similarity (LPIPS* ↓*)*[\[52\]](#page-10-12): the perceptual image similarity between the target image and the reconstructed image measured by a VGG network [\[42\]](#page-10-13), and (4)*MSE - Representation Space (MSE-R* ↓*)*: the MSE between the target image and the reconstructed image measured in the learned representation space, i.e., the feature vector before the final classification layer [\[44\]](#page-10-6). Note that "↓" means the lower the metric the higher relative image quality, while "↑" represents the higher the metric the higher image quality.

## 2. Choice of Loss Function

We first evaluate the performance of different loss function configurations. We randomly select 10 images from the evaluation set of the CelebA dataset and measure the mean and standard deviation of the MSE-I and PSNR scores between the original images and their reconstructions using Adam optimizer. From results presented in Table [1](#page-4-0) we observe that using squared `<sup>2</sup> norm (D1) for computing the gradient matching loss with KLD as the regularization term (R1) yields the best reconstructed image quality. Therefore, hereinafter we use this loss configuration for analyzing the impact of different optimizers and defenses.

## 3. Choice of Optimization Strategy

We next study the impact of different optimizers on the reconstruction results. We randomly select images from the CelebA and ImageNet dataset to compute the reconstruction and repeat the experiment by varying its random seed. The numbers of updates are set to 2500, 1000, and 800 for Adam, BO, and CMA-ES, respectively. We summarize the results in Table [2](#page-4-1) and provide visualization of the reconstruction samples in Figure [3.](#page-4-2) We find that the gradient-based and gradient-free optimizers show similar performance on the CelebA dataset, with Adam performing slightly better both visually and statistically. However, on the ImageNet dataset, the gradient-based Adam optimizer fails to recover any useful information from the gradients other than the class label. Moreover, its reconstruction results are highly dependent on the initialization. The gradient-free optimizers (BO and CMA-ES), on the other hand, are still able to find samples that resemble the original private image and are more resilient to different initialization conditions. The reason causing this performance difference is twofold: (1) the images in the CelebA dataset are well-aligned, while the ImageNet dataset has a more heterogeneous data distribution; and (2) the generator used for generating high-resolution ImageNet data has a deeper and more complex structure, which makes it hard for gradientbased optimizers to find a projection in its latent space. Based on this observation, we choose to use CMA-ES as the optimizer for conducting experiments under various defense settings.

## <span id="page-5-0"></span>4.4. Comparison with Existing Gradient Leakage Attacks Under Defenses

Attack Baselines. We compare our method with several state-of-the-art attack methods: (1) *Deep Leakage from Gradients (DLG)*[\[56\]](#page-10-4): gradient leakage attack with `<sup>2</sup> gradient matching loss and L-BFGS optimizer; (2)*Improved Deep Leakage from Gradients (iDLG)*[\[54\]](#page-10-3): improved DLG attack with label inference; (3)*Inverting Gradients (IG)*[\[13\]](#page-9-7): gradient leakage attack with cosine distance as loss and total variation as prior, optimized using Adam; and (4)*GradInversion (GI)*[\[51\]](#page-10-2): gradient leakage attack with `<sup>2</sup> gradient matching loss and Adam optimizer.

We implemented these attacks following the code repositories released by the authors [\[12,](#page-8-11)[53,](#page-10-14)[55\]](#page-10-15). In our implementation of GI, we consider a stricter scenario where the batch normalization statistics are unknown to the adversary. For the second-order-based DLG and iDLG attacks, we use the L-BFGS optimizer to conduct 300 iterations of optimization on the CelebA dataset and 1, 200 iterations on the ImageNet dataset to reconstruct the data. As for the first-order-based IG and GI attacks, we use the Adam optimizer with an initial learning rate of 0.1 and conduct 8, 000 iterations of optimization on CelebA and 24, 000 iterations on ImageNet. The performance of several existing methods is highly varying according to different random seeds. To mitigate this, each attack is given 4 trials and the best result with the lowest loss is selected as its final reconstruction.

### Defense Scheme.

Following prior studies [\[44,](#page-10-6) [56\]](#page-10-4), we choose a relatively strict defense setting for conducting evaluation: (1)*Additive*<span id="page-6-2"></span><span id="page-6-0"></span>![](_page_6_Figure_0.jpeg)

Figure 4. Comparison of the reconstruction results with attack baselines on the CelebA & ImageNet datasets under various privacy defenses.
*Noise*[\[44,](#page-10-6) [56\]](#page-10-4): inject a Gaussian noise ε ∼ N (0, σ<sup>2</sup> I) to the gradients with σ = 0.1; (2)*Gradient Clipping*[\[14,](#page-9-9) [48\]](#page-10-5): clip the values of the gradients with a bound of S = 4; (3)*Gradient Spasification*[\[56\]](#page-10-4): perform magnitude-based pruning on the gradients to achieve 90% sparsity; and (4)*Soteria*[\[44\]](#page-10-6): gradients are generated on the perturbed representation with a pruning rate of 80%.

Results. Table [3](#page-5-1) compares the performance of the proposed method GGL with other gradient leakage attack methods. Our general observation is that existing attack methods struggle to reconstruct a realistic image with the present of any privacy defense mechanism, while the proposed GGL is able to synthesize high quality images that are similar to the original ones, with the measured PSNR >10.1 on the CelebA dataset and >5.7 on ImageNet dataset across all scenarios. One exception is that we find the gradient clipping operation has a very low effect on the IG attack. This is because clipping to `<sup>2</sup> norm only changes the magnitude of the gradients and does not affect the angular information (i.e., direction). Therefore, though gradient clipping increases the reconstruction error for attacks based on the Euclidean distance between gradients, it will not affect the IG attack which utilizes the magnitude-invariant cosine distance for computing its gradient matching loss. Clipping to L<sup>∞</sup> norm instead would address this issue, however, it is not adopted by existing DP mechanisms as it will result in a poor `<sup>2</sup> bound. We also notice that comparing to gradient sparsification, reconstructing from the gradients produced from the perturbed data representation using the Soteria defense would result in higher MSE in both the image space and the representation space, especially on the ImageNet dataset. Despite this, such defense can still be bypassed by our adaptive attack.

From the visualization results in Figure [4,](#page-6-0) we can see that except for the IG attack in the case of gradient clipping, the reconstructed image of existing attacks does not

<span id="page-6-1"></span>![](_page_6_Figure_5.jpeg)

Figure 5. Reconstruction results against the Soteria [\[44\]](#page-10-6) defense on the ImageNet dataset: (top) original image and its (bottom) reconstruction by GGL.

reveal much information about the original image. We also observe that on the CelebA dataset, the proposed method GGL isn't able to reconstruct the exact face of the person in the original image when defenses are applied, yet it successfully reveals several key attributes including gender, hair style, hair color, skin color, head posture, and even the background color. Even on the more challenging ImageNet dataset, our method can still produce a high quality reconstruction that reveals the composition of the original image under these defenses. More samples on the ImageNet dataset against the Soteria defense is presented in Figure [5.](#page-6-1)

Combining Clipping and Noise Addition. In addition, we also evaluate our attack against the combination of multiple defense mechanisms. Figure [6](#page-7-0) compares the reconstruction results under 3 defense settings: additive noise with σ = 0.1, gradient clipping with S = 4, and simultaneously applying gradient clipping and additive noise (i.e., the privacy defense used in local and distributed DP). We observe that the high-resolution image can still be reconstructed under these defenses, and combining gradient clipping and additive noise would lead to a relatively worse re-

<span id="page-7-2"></span><span id="page-7-0"></span>![](_page_7_Figure_0.jpeg)

Figure 6. Illustration of combined defense: (left) original image and its (right) reconstruction by GGL. The PSNR with respect to the original image is shown below each reconstructed image.

construction with the lowest PSNR. We thus believe this attack can also be used as an auditing measurement for local differential privacy.

## 5. Impact of Defense Parameter

We next apply the Soteria [\[44\]](#page-10-6) defense on the CelebA dataset as a case study to investigate the impact of different defense parameters. We use the attack baselines and the proposed GGL to generate reconstructions as we vary the pruning rate from 0% to 80%, and summarize the results in Figure [7.](#page-7-1) The authors reported in their original paper [\[44\]](#page-10-6) that the DLG [\[56\]](#page-10-4) and IG [\[13\]](#page-9-7) attack can tolerate the Soteria defense with a pruning rate up to 40% on the CIFAR10 dataset. Differently, we observe that on the CelebA dataset, defense with a low pruning rate of 10% would already impose a significant impact on the reconstruction results of these attacks. This is perhaps because the Soteria defense mainly affects the fully-connected layer that produces class-level data representation. Different from CIFAR10, the class-wise label of the CelebA dataset does not directly reveal contextual information about the subject (e.g., the identity of the person). Instead, it only encodes very coarse-grained information (i.e., gender) and thus can be more susceptible to perturbations. In other words, privacy information that is entangled with the class label is more likely to be leaked through gradients. Nevertheless, the proposed method can still reliably recover the profile of the person from the remaining gradients regardless of the pruning rate.

# Discussion

Limitation. Although the image prior captured by the GAN model can help restore the missing information from the degraded gradients for better image reconstruction, at the same time the output image distribution is also constrained by the GAN latent space, rendering it hard to faithfully reconstruct out-of-distribution image samples. Figure [8](#page-8-12) shows two examples of attempting to reconstruct out-of-distribution ImageNet images under the Soteria defense [\[44\]](#page-10-6): in Figure [8a,](#page-8-12) the orientation of the object reconstructed image is changed from the original image; and

<span id="page-7-1"></span>![](_page_7_Figure_7.jpeg)

Figure 7. Reconstruction results under the Soteria [\[44\]](#page-10-6) defense with varying pruning rates on the CelebA dataset. The PSNR with respect to the original image is shown below each reconstructed image.

Figure [8b,](#page-8-12) the reconstruction result is missing important semantics (e.g., the person) that is not well-represented in its class (i.e., Bernese mountain dog). These phenomena can potentially be improved by jointly optimizing the class condition [\[25\]](#page-9-23) or relaxing the generator [\[39\]](#page-9-27).

Analysis of Loss Landscape and Potential Defense. To investigate the reconstruction problem under the constraint of a generative model, we use the latent vector returned by GGL as the central point and choose two directions to visualize the loss landscape of the gradient matching loss as well as the LPIPS loss between the original image and the image generated by the BigGAN model by sampling in the latent space. The visualization results are presented in Figure [9,](#page-8-13) where Figure [9a](#page-8-13) shows the loss landscape observed by the adversary if only the gradient information is accessible, and Figure [9b](#page-8-13) shows the ground truth loss landscape measured by the LPIPS score assuming the original image is known. We have the following two observations: (1) the surface of the gradient matching loss is non-convex and contains several local minima; and (2) there exists an inconsistency between the ground truth and the observed loss surface, i.e., the image found by optimizing the gradient matching loss doesn't provide the most similar visual result. However, as showed in our experiments, such a level of inconsistency isn't sufficient to provide privacy guarantees as the suboptimal result with minimized gradient matching loss still leaks a considerable amount of information about the original image. This hints us that applying transformations to the gradients to reform the gradient matching loss so that its landscape is no longer in line with the ground truth LPIPS loss

<span id="page-8-12"></span>![](_page_8_Figure_0.jpeg)

(a) Change in orientation (b) Missing semantics

Figure 8. Reconstruction results of out-of-distribution image samples: (left) original image and its (right) reconstruction by GGL.

<span id="page-8-13"></span>![](_page_8_Figure_4.jpeg)

Figure 9. Visualization of the loss landscapes.

can help to effectively achieve privacy preservation against generative gradient leakage attacks.

# Conclusion

This work presents Generative Gradient Leakage (GGL), an approach that utilizes a generative model to extract prior information from public datasets to improve image reconstruction from degraded gradients produced by privacy defenses. Our experimental results on two image classification datasets show that with the learned image prior, the proposed method is more resilient to the perturbations and lossy transformations applied to the gradients and is still able to reconstruct high-fidelity images that reveal information about the original images when existing attacks all fail. We hope the proposed method can serve as an analysis tool for empirical privacy auditing to help facilitate the future design of privacy defenses.

# Acknowledgement

The authors would like to thank Peter Kairouz from Google Research for his valuable feedback on the paper. This work is supported in part by NSF CNS-2114161, ECCS-2132106, CBET-2130643, the Science Alliance's StART program, and the GCP credits provided by Google Cloud. This work is also supported by the U.S. Department of Energy, Office of Science, Office of Advanced Scientific Computing Research, Applied Mathematics program; and by the Artificial Intelligence Initiative at the Oak Ridge National Laboratory (ORNL). ORNL is operated by UT- Battelle, LLC., for the U.S. Department of Energy under Contract DEAC05-00OR22725.

# References

- <span id="page-8-6"></span>[1] Nitin Agrawal, Ali Shahin Shamsabadi, Matt J Kusner, and Adria Gasc ` on. Quotient: two-party secure neural network ´ training and prediction. In*Proceedings of the 2019 ACM SIGSAC Conference on Computer and Communications Security*, pages 1231–1247, 2019. [3](#page-2-2)
- <span id="page-8-7"></span>[2] Amir Beck and Marc Teboulle. Fast gradient-based algorithms for constrained total variation image denoising and deblurring problems. *IEEE transactions on image processing*, 18(11):2419–2434, 2009. [3](#page-2-2)
- <span id="page-8-8"></span>[3] Ashish Bora, Ajil Jalal, Eric Price, and Alexandros G Dimakis. Compressed sensing using generative models. In *International Conference on Machine Learning*, pages 537– 546. PMLR, 2017. [4](#page-3-1)
- <span id="page-8-0"></span>[4] Theodora S Brisimi, Ruidi Chen, Theofanie Mela, Alex Olshevsky, Ioannis Ch Paschalidis, and Wei Shi. Federated learning of predictive models from federated electronic health records. *International journal of medical informatics*, 112:59–67, 2018. [1](#page-0-2)
- <span id="page-8-10"></span>[5] Andrew Brock and Alex Andonian. BigGAN PyTorch Implementation. [https://github.com/ajbrock/](https://github.com/ajbrock/BigGAN-PyTorch) [BigGAN-PyTorch](https://github.com/ajbrock/BigGAN-PyTorch). Accessed: 2021-11-09. [5](#page-4-3)
- <span id="page-8-2"></span>[6] Andrew Brock, Jeff Donahue, and Karen Simonyan. Large scale gan training for high fidelity natural image synthesis. In *International Conference on Learning Representations*, 2018. [2,](#page-1-0) [5,](#page-4-3) [12](#page-11-0)
- <span id="page-8-9"></span>[7] Dingfan Chen, Ning Yu, Yang Zhang, and Mario Fritz. Ganleaks: A taxonomy of membership inference attacks against generative models. In *Proceedings of the 2020 ACM SIGSAC conference on computer and communications security*, pages 343–362, 2020. [5](#page-4-3)
- <span id="page-8-1"></span>[8] Olivia Choudhury, Yoonyoung Park, Theodoros Salonidis, Aris Gkoulalas-Divanis, Issa Sylla, et al. Predicting adverse drug reactions on distributed health data using federated learning. In *AMIA Annual symposium proceedings*, volume 2019, page 313. American Medical Informatics Association, 2019. [1](#page-0-2)
- <span id="page-8-4"></span>[9] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database. In *2009 IEEE conference on computer vision and pattern recognition*, pages 248–255. Ieee, 2009. [2,](#page-1-0) [5](#page-4-3)
- <span id="page-8-3"></span>[10] David Eriksson, Michael Pearce, Jacob Gardner, Ryan D Turner, and Matthias Poloczek. Scalable global optimization via local bayesian optimization. *Advances in Neural Information Processing Systems*, 32:5496–5507, 2019. [2,](#page-1-0) [5,](#page-4-3) [12](#page-11-0)
- <span id="page-8-5"></span>[11] Karan Ganju, Qi Wang, Wei Yang, Carl A Gunter, and Nikita Borisov. Property inference attacks on fully connected neural networks using permutation invariant representations. In *Proceedings of the ACM SIGSAC Conference on Computer and Communications Security (CCS)*, pages 619–633, 2018. [2](#page-1-0)
- <span id="page-8-11"></span>[12] Jonas Geiping, Hartmut Bauermeister, Hannah Droge, ¨ and Michael Moeller. Inverting Gradients Implemen-

tation. [https://github.com/JonasGeiping/](https://github.com/JonasGeiping/invertinggradients) [invertinggradients](https://github.com/JonasGeiping/invertinggradients). Accessed: 2021-11-09. [6](#page-5-2)

- <span id="page-9-7"></span>[13] Jonas Geiping, Hartmut Bauermeister, Hannah Droge, and ¨ Michael Moeller. Inverting gradients-how easy is it to break privacy in federated learning? *Advances in Neural Information Processing Systems*, 33:16937–16947, 2020. [1,](#page-0-2) [2,](#page-1-0) [3,](#page-2-2) [4,](#page-3-1) [5,](#page-4-3) [6,](#page-5-2) [8,](#page-7-2) [13](#page-12-0)
- <span id="page-9-9"></span>[14] Robin C Geyer, Tassilo Klein, and Moin Nabi. Differentially private federated learning: A client level perspective. *arXiv preprint arXiv:1712.07557*, 2017. [1,](#page-0-2) [3,](#page-2-2) [4,](#page-3-1) [6,](#page-5-2) [7,](#page-6-2) [11](#page-10-16)
- <span id="page-9-11"></span>[15] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio. Generative adversarial nets. *Advances in neural information processing systems*, 27, 2014. [2](#page-1-0)
- <span id="page-9-4"></span>[16] Filip Granqvist, Matt Seigel, Rogier van Dalen, Aine Cahill, ´ Stephen Shum, and Matthias Paulik. Improving on-device speaker verification using federated learning with privacy. In *Interspeech*, pages 4328–4332, 2020. [1](#page-0-2)
- <span id="page-9-26"></span>[17] Ishaan Gulrajani, Faruk Ahmed, Martin Arjovsky, Vincent Dumoulin, and Aaron Courville. Improved training of wasserstein gans. *arXiv preprint arXiv:1704.00028*, 2017. [5,](#page-4-3) [12](#page-11-0)
- <span id="page-9-24"></span>[18] Nikolaus Hansen. The cma evolution strategy: a comparing review. *Towards a new evolutionary computation*, pages 75– 102, 2006. [5](#page-4-3)
- <span id="page-9-13"></span>[19] Nikolaus Hansen. The cma evolution strategy: A tutorial. *arXiv preprint arXiv:1604.00772*, 2016. [2,](#page-1-0) [5](#page-4-3)
- <span id="page-9-5"></span>[20] Andrew Hard, Kurt Partridge, Cameron Nguyen, Niranjan Subrahmanya, Aishanee Shah, Pai Zhu, Ignacio Lopez Moreno, and Rajiv Mathews. Training keyword spotting models on non-iid data with federated learning. *arXiv preprint arXiv:2005.10406*, 2020. [1](#page-0-2)
- <span id="page-9-3"></span>[21] Andrew Hard, Kanishka Rao, Rajiv Mathews, Swaroop Ramaswamy, Franc¸oise Beaufays, Sean Augenstein, Hubert Eichner, Chloe Kiddon, and Daniel Ramage. Federated ´ learning for mobile keyboard prediction. *arXiv preprint arXiv:1811.03604*, 2018. [1](#page-0-2)
- <span id="page-9-19"></span>[22] Stephen Hardy, Wilko Henecka, Hamish Ivey-Law, Richard Nock, Giorgio Patrini, Guillaume Smith, and Brian Thorne. Private federated learning on vertically partitioned data via entity resolution and additively homomorphic encryption. *arXiv preprint arXiv:1711.10677*, 2017. [3](#page-2-2)
- <span id="page-9-17"></span>[23] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. In *Proceedings of the IEEE conference on computer vision and pattern recognition*, pages 770–778, 2016. [2,](#page-1-0) [5](#page-4-3)
- <span id="page-9-16"></span>[24] Briland Hitaj, Giuseppe Ateniese, and Fernando Perez-Cruz. Deep models under the gan: information leakage from collaborative deep learning. In *Proceedings of the ACM SIGSAC Conference on Computer and Communications Security (CCS)*, pages 603–618, 2017. [2](#page-1-0)
- <span id="page-9-23"></span>[25] Minyoung Huh, Richard Zhang, Jun-Yan Zhu, Sylvain Paris, and Aaron Hertzmann. Transforming and projecting images into class-conditional generative networks. In *European Conference on Computer Vision*, pages 17–34. Springer, 2020. [5,](#page-4-3) [8,](#page-7-2) [12](#page-11-0)
- <span id="page-9-0"></span>[26] Peter Kairouz, H Brendan McMahan, Brendan Avent, Aurelien Bellet, Mehdi Bennis, Arjun Nitin Bhagoji, Kallista ´

Bonawitz, Zachary Charles, Graham Cormode, Rachel Cummings, et al. Advances and open problems in federated learning. *arXiv preprint arXiv:1912.04977*, 2019. [1](#page-0-2)

- <span id="page-9-12"></span>[27] Tero Karras, Samuli Laine, Miika Aittala, Janne Hellsten, Jaakko Lehtinen, and Timo Aila. Analyzing and improving the image quality of stylegan. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 8110–8119, 2020. [2](#page-1-0)
- <span id="page-9-22"></span>[28] Diederik P Kingma and Max Welling. Auto-encoding variational bayes. *arXiv preprint arXiv:1312.6114*, 2013. [5](#page-4-3)
- <span id="page-9-1"></span>[29] Tian Li, Anit Kumar Sahu, Ameet Talwalkar, and Virginia Smith. Federated learning: Challenges, methods, and future directions. *IEEE Signal Processing Magazine*, 37(3):50–60, 2020. [1](#page-0-2)
- <span id="page-9-21"></span>[30] Yujun Lin, Song Han, Huizi Mao, Yu Wang, and Bill Dally. Deep gradient compression: Reducing the communication bandwidth for distributed training. In *International Conference on Learning Representations*, 2018. [4](#page-3-1)
- <span id="page-9-14"></span>[31] Ziwei Liu, Ping Luo, Xiaogang Wang, and Xiaoou Tang. Deep learning face attributes in the wild. In *Proceedings of International Conference on Computer Vision (ICCV)*, December 2015. [2,](#page-1-0) [5](#page-4-3)
- <span id="page-9-6"></span>[32] Guodong Long, Yue Tan, Jing Jiang, and Chengqi Zhang. Federated learning for open banking. In *Federated learning*, pages 240–254. Springer, 2020. [1](#page-0-2)
- <span id="page-9-10"></span>[33] Aravindh Mahendran and Andrea Vedaldi. Understanding deep image representations by inverting them. In *Proceedings of the IEEE conference on computer vision and pattern recognition*, pages 5188–5196, 2015. [2](#page-1-0)
- <span id="page-9-2"></span>[34] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. Communicationefficient learning of deep networks from decentralized data. In *Artificial intelligence and statistics*, pages 1273–1282. PMLR, 2017. [1](#page-0-2)
- <span id="page-9-8"></span>[35] Luca Melis, Congzheng Song, Emiliano De Cristofaro, and Vitaly Shmatikov. Exploiting unintended feature leakage in collaborative learning. In *2019 IEEE Symposium on Security and Privacy (SP)*, pages 691–706. IEEE, 2019. [1,](#page-0-2) [2,](#page-1-0) [3](#page-2-2)
- <span id="page-9-20"></span>[36] Mehdi Mirza and Simon Osindero. Conditional generative adversarial nets. *arXiv preprint arXiv:1411.1784*, 2014. [4](#page-3-1)
- <span id="page-9-18"></span>[37] Payman Mohassel and Yupeng Zhang. Secureml: A system for scalable privacy-preserving machine learning. In *2017 IEEE symposium on security and privacy (SP)*, pages 19–38. IEEE, 2017. [3](#page-2-2)
- <span id="page-9-15"></span>[38] Milad Nasr, Reza Shokri, and Amir Houmansadr. Comprehensive privacy analysis of deep learning: Passive and active white-box inference attacks against centralized and federated learning. In *Proceedings of the IEEE symposium on security and privacy (SP)*, pages 739–753. IEEE, 2019. [2](#page-1-0)
- <span id="page-9-27"></span>[39] Xingang Pan, Xiaohang Zhan, Bo Dai, Dahua Lin, Chen Change Loy, and Ping Luo. Exploiting deep generative prior for versatile image restoration and manipulation. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 2021. [8](#page-7-2)
- <span id="page-9-25"></span>[40] Alec Radford, Luke Metz, and Soumith Chintala. Unsupervised representation learning with deep convolutional generative adversarial networks. *arXiv preprint arXiv:1511.06434*, 2015. [5,](#page-4-3) [12](#page-11-0)

- <span id="page-10-16"></span><span id="page-10-0"></span>[41] Adam Sadilek, Luyang Liu, Dung Nguyen, Methun Kamruzzaman, Stylianos Serghiou, Benjamin Rader, Alex Ingerman, Stefan Mellem, Peter Kairouz, Elaine O Nsoesie, et al. Privacy-first health research with federated learning. *NPJ digital medicine*, 4(1):1–8, 2021. [1](#page-0-2)
- <span id="page-10-13"></span>[42] Karen Simonyan and Andrew Zisserman. Very deep convolutional networks for large-scale image recognition. *arXiv preprint arXiv:1409.1556*, 2014. [6](#page-5-2)
- <span id="page-10-11"></span>[43] Jasper Snoek, Hugo Larochelle, and Ryan P Adams. Practical bayesian optimization of machine learning algorithms. *Advances in neural information processing systems*, 25, 2012. [5](#page-4-3)
- <span id="page-10-6"></span>[44] Jingwei Sun, Ang Li, Binghui Wang, Huanrui Yang, Hai Li, and Yiran Chen. Soteria: Provable defense against privacy leakage in federated learning from representation perspective. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 9311–9319, 2021. [1,](#page-0-2) [3,](#page-2-2) [4,](#page-3-1) [6,](#page-5-2) [7,](#page-6-2) [8,](#page-7-2) [11,](#page-10-16) [12,](#page-11-0) [13](#page-12-0)
- <span id="page-10-9"></span>[45] Stacey Truex, Nathalie Baracaldo, Ali Anwar, Thomas Steinke, Heiko Ludwig, Rui Zhang, and Yi Zhou. A hybrid approach to privacy-preserving federated learning. In *Proceedings of the 12th ACM Workshop on Artificial Intelligence and Security*, pages 1–11, 2019. [3](#page-2-2)
- <span id="page-10-10"></span>[46] Dave Van Veen, Ajil Jalal, Mahdi Soltanolkotabi, Eric Price, Sriram Vishwanath, and Alexandros G Dimakis. Compressed sensing with deep image prior and learned regularization. *arXiv preprint arXiv:1806.06438*, 2018. [4](#page-3-1)
- <span id="page-10-7"></span>[47] Zhibo Wang, Mengkai Song, Zhifei Zhang, Yang Song, Qian Wang, and Hairong Qi. Beyond inferring class representatives: User-level privacy leakage from federated learning. In *Proceedings of the IEEE Conference on Computer Communications (INFOCOM)*, pages 2512–2520. IEEE, 2019. [2](#page-1-0)
- <span id="page-10-5"></span>[48] Wenqi Wei, Ling Liu, Yanzhao Wut, Gong Su, and Arun Iyengar. Gradient-leakage resilient federated learning. In *2021 IEEE 41st International Conference on Distributed Computing Systems (ICDCS)*, pages 797–807. IEEE, 2021. [1,](#page-0-2) [3,](#page-2-2) [4,](#page-3-1) [6,](#page-5-2) [7,](#page-6-2) [11](#page-10-16)
- <span id="page-10-8"></span>[49] Guowen Xu, Hongwei Li, Sen Liu, Kan Yang, and Xiaodong Lin. Verifynet: Secure and verifiable federated learning. *IEEE Transactions on Information Forensics and Security*, 15:911–926, 2019. [3](#page-2-2)
- <span id="page-10-1"></span>[50] Wensi Yang, Yuhang Zhang, Kejiang Ye, Li Li, and Cheng-Zhong Xu. Ffd: A federated learning based method for credit card fraud detection. In *International conference on big data*, pages 18–32. Springer, 2019. [1](#page-0-2)
- <span id="page-10-2"></span>[51] Hongxu Yin, Arun Mallya, Arash Vahdat, Jose M Alvarez, Jan Kautz, and Pavlo Molchanov. See through gradients: Image batch recovery via gradinversion. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 16337–16346, 2021. [1,](#page-0-2) [2,](#page-1-0) [3,](#page-2-2) [4,](#page-3-1) [5,](#page-4-3) [6,](#page-5-2) [13](#page-12-0)
- <span id="page-10-12"></span>[52] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang. The unreasonable effectiveness of deep features as a perceptual metric. In *Proceedings of the IEEE conference on computer vision and pattern recognition*, pages 586–595, 2018. [6](#page-5-2)
- <span id="page-10-14"></span>[53] Bo Zhao, Konda Reddy Mopuri, and Hakan Bilen. Improved Deep Leakage from Gradients Implementation. [https:](https://github.com/PatrickZH/Improved-Deep-Leakage-from-Gradients)

[/ / github . com / PatrickZH / Improved - Deep -](https://github.com/PatrickZH/Improved-Deep-Leakage-from-Gradients) [Leakage-from-Gradients](https://github.com/PatrickZH/Improved-Deep-Leakage-from-Gradients). Accessed: 2021-11-09. [6](#page-5-2)

- <span id="page-10-3"></span>[54] Bo Zhao, Konda Reddy Mopuri, and Hakan Bilen. idlg: Improved deep leakage from gradients. *arXiv preprint arXiv:2001.02610*, 2020. [1,](#page-0-2) [2,](#page-1-0) [3,](#page-2-2) [4,](#page-3-1) [5,](#page-4-3) [6](#page-5-2)
- <span id="page-10-15"></span>[55] Ligeng Zhu and Song Han. Deep Leakage from Gradients Implementation. [https://github.com/mit-han](https://github.com/mit-han-lab/dlg)[lab/dlg](https://github.com/mit-han-lab/dlg). Accessed: 2021-11-09. [6](#page-5-2)
- <span id="page-10-4"></span>[56] Ligeng Zhu and Song Han. Deep leakage from gradients. In *Federated learning*, pages 17–31. Springer, 2020. [1,](#page-0-2) [2,](#page-1-0) [3,](#page-2-2) [4,](#page-3-1) [5,](#page-4-3) [6,](#page-5-2) [7,](#page-6-2) [8,](#page-7-2) [11,](#page-10-16) [13](#page-12-0)

# A. Additional Reconstruction Samples

Due to page limit, we only include the reconstruction results under the Soteria [\[44\]](#page-10-6) defense in our main paper (Figure [5\)](#page-6-1) for additional visualization samples on the ImageNet dataset. Here we present the full results under all 4 considered defenses (i.e., additive noise [\[44,](#page-10-6) [56\]](#page-10-4) with σ = 0.1, gradient clipping [\[14,](#page-9-9) [48\]](#page-10-5) with S = 4, gradient spasification [\[56\]](#page-10-4) with a pruning rate of 90%, and Soteria [\[44\]](#page-10-6) with a pruning rate of 80%) in Figure [10.](#page-10-17) We observe that our method is able to reconstruct high-quality images from gradients in all these considered cases regardless of the type of defense.

<span id="page-10-17"></span>![](_page_10_Picture_19.jpeg)

Figure 10. Reconstruction results under various defenses on the ImageNet dataset: (first row) original images and (the rest of rows) their reconstructions by GGL under various defenses.

# <span id="page-11-0"></span>B. Implementation Details

Optimization Configuration. We use the following configuration for the explored optimizers: (1) *Adam*: initial learning rate lr = 0.1, β<sup>1</sup> = 0.9, β<sup>2</sup> = 0.999. On the CelebA dataset, we use a step learning rate decay at step 937, 1562, and 2189, by a factor of γ = 0.1. On the ImageNet dataset, the learning rate is linearly warmed-up from 0 during the first 125 iterations and gradually reduced to 0 in the last 625 iterations using cosine decay; (2) *BO*: We use the *TurBO-1*algorithm [\[10\]](#page-8-3) with 256 initial points, batch size = 10, lower bound = −2, upper bound = 2, and automatic relevance determination (ARD) kernel for the Gaussian process; and (3)*CMA-ES*: we use random initialization with batch size = 50. We set λ = 0.1 for experiments on the CelebA dataset. On the ImageNet dataset, for algorithms that do not innately support bound constraints, we apply the *tanh*function to achieve the bound.

GAN Configuration. For the CelebA dataset, we train a DCGAN [\[40\]](#page-9-25) with a latent dimension of 128 with its detailed structure presented in Figure [11.](#page-11-1) Specifically, we use the Wasserstein distance with the loss weight set to 10 for the gradient penalty [\[17\]](#page-9-26). The GAN model is trained for 100 epochs using Adam optimizer with a learning rate of 0.0001 and a batch size of 64. For the ImageNet dataset, we use a pre-trained BigGAN [\[6\]](#page-8-2) with a latent dimension of 128 and output image size of 256 × 256. The output image is further rescaled to 224 × 224 for computing the FL task.

<span id="page-11-1"></span>

| Type              | Kernel | Stride | Output |  |  |  |  |  |  |
|-------------------|--------|--------|--------|--|--|--|--|--|--|
| FC                |        |        | 8192   |  |  |  |  |  |  |
| BN1D              |        |        | 8192   |  |  |  |  |  |  |
| DeConv2D          | 2 × 2  | 2 × 2  | 256    |  |  |  |  |  |  |
| BN2D              |        |        | 256    |  |  |  |  |  |  |
| DeConv2D          | 2 × 2  | 2 × 2  | 128    |  |  |  |  |  |  |
| BN2D              |        |        | 128    |  |  |  |  |  |  |
| DeConv2D          | 2 × 2  | 2 × 2  | 3      |  |  |  |  |  |  |
| (a) Generator     |        |        |        |  |  |  |  |  |  |
| Type              | Kernel | Stride | Output |  |  |  |  |  |  |
| Conv2D            | 3 × 3  | 2 × 2  | 128    |  |  |  |  |  |  |
| Conv2D            | 3 × 3  | 2 × 2  | 256    |  |  |  |  |  |  |
| Conv2D            | 3 × 3  | 2 × 2  | 512    |  |  |  |  |  |  |
| FC                |        |        | 1      |  |  |  |  |  |  |
| (b) Discriminator |        |        |        |  |  |  |  |  |  |

Figure 11. GAN structure for the CelebA dataset.

# C. Loss Landscape Analysis

Comparison with GAN Inversion. In our attack, we consider the private image to be unknown and the adversary attempts to reconstruct the image from the shared gradient information using a pre-trained GAN. However, such reconstruction is constrained by the generator's fitting abil-

<span id="page-11-2"></span>![](_page_11_Figure_7.jpeg)

Figure 12. Comparison of image reconstructed by our method and GAN inversion.

ity. GAN inversion technique which inverts a given image to the GAN's latent space can serve as a means for testing the upper bound of the image quality reconstructed from GAN. To evaluate, we compare the reconstructed image from gradients using our method and the inverted image using GAN inversion technique [\[25\]](#page-9-23). To compare the information provided by gradient information with the information provided by the original image, we further visualize the gradient matching loss and the LPIPS loss in the GAN latent space. Specifically, we plot the loss functions by interpolating between the latent vectors found by the proposed GGL (z1) and GAN inversion (z2): z(α) = (1−α)z1+αz2. From the results presented in Figure [12](#page-11-2) we observe that (1) the latent vector found by our method does yield the lowest gradient matching loss on this line; (2) compared to the gradient information, the information provided by the original image can better guide the optimization process in the GAN latent space: the latent vector found by GAN inversion produces a better image quality (lower LPIPS) than the solution found by our method; and (3) the latent vector with the lowest gradient match loss doesn't result in the best image quality/similarity (measured by LPIPS).

Different Defenses. We next analyze how each defense mechanism affects the loss landscape. We extend the visualization to a 2D surface by adding a second random direction vector η (normalized according to z<sup>2</sup> − z1): z(α, β) = z<sup>1</sup> + α(z<sup>2</sup> − z1) + βη. Figure [13](#page-12-1) shows the visualized loss surface under different defense settings. We can see that additive noise and gradient sparsification do not have much impact on the geometric landscape of the gradient matching loss, whereas gradient clipping and Soteria [\[44\]](#page-10-6) clearly deform the gradient matching loss surface, rendering it hard for the adversary to find a good reconstruction under such defenses. However, by applying the adaptive transformation at the adversary's side, such deforma<span id="page-12-0"></span>tion can be greatly mitigated and thereby enables the adversary to reconstruct high-quality images even with the presence of these defenses.

<span id="page-12-1"></span>![](_page_12_Figure_1.jpeg)

Figure 13. Visualization of observed loss landscapes under various defense settings. The bottom 3 rows compare the loss surface with (right) and without (left) applying adaptive transformation at the adversary's side.

# D. Larger Batch Sizes or Multiple Local Steps

Recovering high-resolution batch data with multiple local steps remains a major challenge in this line of research. Most existing studies [\[13,](#page-9-7) [56\]](#page-10-4) only work on small images (32×32px) for batch size > 1. Currently, the only study that accounts for local steps > 1 is IG [\[13\]](#page-9-7), but it only works on a single ImageNet image. The only study that can work on batched full-size ImageNet images (224×224px) is GI [\[51\]](#page-10-2), which supports up to 48 images with local step = 1. However, it can only reveal limited information from partial images of the batch, and it assumes that the BatchNorm (BN) statistics (mean and std.) of the target batch is jointly provided with the gradients and only works for specially pretrained large ResNet-50 model (larger model provides more gradient information).

Differently, we seek to investigate the privacy leakage under various defense strategies. We show that even with batch size = 1 and local step size = 1, existing methods still failed to reconstruct the input under defenses, while our method can reveal a good amount of visual information.

To investigate the generalizability of GGL, we conducted additional experiments on batched ImageNet images (224×224px) and with multiple local steps, with the results presented in Figure [14](#page-12-2) and Figure [15,](#page-12-3) respectively. We can see that GGL can still restore a decent amount of visual information under these settings. The proposed GGL can be further strengthened with additional prior information (e.g., BN statistics).

<span id="page-12-2"></span>![](_page_12_Picture_8.jpeg)

Figure 14. Image reconstruction with batch size = 4: (1st row) original images, (2nd row) reconstructions by GGL w/o defense, and (3rd row) reconstructions by GGL w/ Soteria [\[44\]](#page-10-6) defense.

<span id="page-12-3"></span>![](_page_12_Figure_10.jpeg)

Figure 15. Reconstruction by GGL with multiple local steps.

<span id="page-12-4"></span>![](_page_12_Picture_12.jpeg)

Figure 16. Reconstruction of*in-the-wild*images: (1st row) images from*Google Images*and (2nd row) their reconstructions by GGL.

# E. Recovering In-the-wild Data

We target the practical scenario where the attacker can utilize all public-accessible data as prior information to launch the attack. Thus we chose to use CelebA and ImageNet for evaluation as they are all Internet-based datasets and are easy to access as an attacker. We also used the disjoint dataset so that the images used for testing haven't been used for GAN training. To investigate the performance of GGL under the scenario where the testing image is not from the GAN training distribution, we conducted additional experiments to recover*in-the-wild* images (i.e., arbitrary images from the search results in Google Images with appropriate cropping/resizing). From the results in Figure [16,](#page-12-4) we can see that GGL can still reveal a reasonable amount of visual information even if the testing images are not from the GAN training distribution.
