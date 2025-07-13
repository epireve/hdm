---
cite_key: mia_2024
title: QuanCrypt-FL: Quantized Homomorphic Encryption with Pruning for Secure Federated Learning
authors: Md Jueal Mia, M. Hadi Amini, Senior Member, IEEE
year: 2020
date_processed: 2025-07-02
phase2_processed: true
original_folder: arxiv_2411.05260_QuanCrypt-FL_Quantized_Homomorphic_Encryption_with_Pruning_for_Secure_Federated_Learning
images_total: 11
images_kept: 11
images_removed: 0
tags: 
keywords: 
---

# QuanCrypt-FL: Quantized Homomorphic Encryption with Pruning for Secure Federated Learning

Md Jueal Mia and M. Hadi Amini, *Senior Member, IEEE*

**Abstract:** —Federated Learning has emerged as a leading approach for decentralized machine learning, enabling multiple clients to collaboratively train a shared model without exchanging private data. While FL enhances data privacy, it remains vulnerable to inference attacks, such as gradient inversion and membership inference, during both training and inference phases. Homomorphic Encryption provides a promising solution by encrypting model updates to protect against such attacks, but it introduces substantial communication overhead, slowing down training and increasing computational costs. To address these challenges, we propose QuanCrypt-FL, a novel algorithm that combines low-bit quantization and pruning techniques to enhance protection against attacks while significantly reducing computational costs during training. Further, we propose and implement mean-based clipping to mitigate quantization overflow or errors. By integrating these methods, QuanCrypt-FL creates a communication-efficient FL framework that ensures privacy protection with minimal impact on model accuracy, thereby improving both computational efficiency and attack resilience. We validate our approach on MNIST, CIFAR-10, and CIFAR-100 datasets, demonstrating superior performance compared to state-of-the-art methods. QuanCrypt-FL consistently outperforms existing method and matches Vanilla-FL in terms of accuracy across varying client. Further, QuanCrypt-FL achieves up to 9x faster encryption, 16x faster decryption, and 1.5x faster inference compared to BatchCrypt, with training time reduced by up to 3x.

**Index Terms:** —Federated Learning, Homomorphic Encryption, Quantization, Pruning, Gradient Inversion, Security.

## I. Introduction

**D**ata is essential for research, driving innovation and discoveries. However, privacy laws like the General Data Protection Regulation (GDPR) and the California Consumer Privacy Act (CCPA) impose strict regulations that complicate how data is collected, used, and shared [[1]](#ref-1) [[2]](#ref-2). Although these laws provide exceptions for research, compliance with requirements such as consent, anonymization, and data minimization is mandatory, thereby making large-scale data collection both challenging and time-consuming [[3]](#ref-3). This creates significant hurdles for deep learning model training, which relies heavily

This work was supported by the National Center for Transportation Cybersecurity and Resiliency (TraCR), a U.S. Department of Transportation National University Transportation Center, headquartered at Clemson University, Clemson, South Carolina, USA.

Manuscript received XXXX; revised XXXX.

on large datasets, as centralized data collection is often restricted by these regulations. As a result, researchers face difficulties navigating legal frameworks, which can substantially slow down the research process [[3]](#ref-3).

Federated Learning (FL) [[4]](#ref-4) offers a promising solution by enabling edge users or organizations to collaboratively train global models by sharing local parameters or gradients without sharing raw data. FL is categorized into cross-device and cross-silo settings. Cross-device FL involves many mobile or IoT devices with limited resources, while cross-silo FL includes fewer organizations with reliable communications and robust computing power [[5]](#ref-5). During FL training, clients share gradients with an honest server to protect data. However, numerous studies have highlighted challenges of indirect data theft through membership inference attacks (MIA) [[6]](#ref-6), [[7]](#ref-7) and gradient inversion attacks (GIA) [[8]](#ref-8)–[[14]](#ref-14). These attacks demonstrate that even without direct access to raw data, an honest-but-curious (or semi-honest) [[15]](#ref-15) server, while following the protocol correctly during FL training, can still infer sensitive information by analyzing the exchanged gradients from the communication channel. Such attacks or vulnerabilities raise questions regarding the real-time applicability of FL in cross-device and cross-silo applications.

Homomorphic Encryption (HE) [[16]](#ref-16)–[[19]](#ref-19) is a widely adopted technique in FL to address security vulnerabilities. HE schemes are categorized based on the number of operations allowed on encrypted data: Partial Homomorphic Encryption (PHE) [[20]](#ref-20), [[21]](#ref-21), Somewhat Homomorphic Encryption (SWHE) [[22]](#ref-22), [[23]](#ref-23), and Fully Homomorphic Encryption (FHE) [[23]](#ref-23), [[24]](#ref-24). These schemes significantly enhance security during the upload and download of model parameters between the server and edge users or organizations in the training phases [[25]](#ref-25), [[26]](#ref-26). HE has therefore been increasingly adopted in various sectors, including healthcare [[27]](#ref-27), finance [[28]](#ref-28), and autonomous systems [[29]](#ref-29). During training, edge users or organizations upload encrypted gradients or parameters using a public key, allowing the server to perform aggregation on the encrypted data without decryption. The updated global model is then sent back to the users for the next round, ensuring that gradients remain secure from the server. In cross-silo FL settings, the Paillier cryptosystem [[21]](#ref-21) is particularly well-suited, as it provides strong privacy guarantees without compromising learning accuracy [[30]](#ref-30), making it a popular choice for secure FL deployments [[31]](#ref-31). However, Paillier is vulnerable to quantum attacks, as its security relies on the hardness of integer factorization, which can be efficiently solved using

Md Jueal Mia and M. Hadi Amini are with The Knight Foundation School of Computing and Information Sciences, Florida International University, Miami, FL 33199. They are also with the Sustainability, Optimization, and Learning for InterDependent networks laboratory (solid lab). (Corresponding author:M. Hadi Amini, email: amini@cs.fiu.edu, hadi.amini@ieee.org)

Shor's algorithm in polynomial time [[32]](#ref-32). To counter this, HE schemes like CKKS [[33]](#ref-33), BGV [[34]](#ref-34), and BFV [[35]](#ref-35), which are based on the hardness of (Ring) Learning with Errors (LWE) problems, are quantum-resistant. Among these, CKKS is particularly advantageous for privacy-preserving machine learning, as it supports real number arithmetic and Single Instruction Multiple Data (SIMD) operations.

However, HE in FL incurs high computational costs due to the mathematical operations, such as addition and multiplication, involved in the training phase [[36]](#ref-36). To address the challenges of high communication costs of HE in FL, techniques like BatchCrypt [[30]](#ref-30) have been developed, utilizing quantization methods to reduce the size of data transmitted during training. By converting high-precision gradients into low-precision integers, these approaches efficiently reduce the communication overhead while maintaining model accuracy. However, BatchCrypt's use of additive encryption limits its capability to perform multiplicative operations on encrypted data, rendering it unsuitable for more advanced optimization techniques that rely on such operations. Additionally, despite its improvements, BatchCrypt remains computationally expensive for large models and datasets, and its design focus on cross-silo FL makes it less suitable for cross-device scenarios where there are many resource-constrained devices with unreliable connections. Further, Yang *et al.* [[37]](#ref-37) utilized the BatchCrypt encryption technique with sparsification to improve FL efficiency. By applying compressive sensing to non-dense layers, they reduced both computational and communication overhead in HE-based systems. Compressive sensing works by transforming model parameters into a sparse signal, where only the essential parameters are retained, and the less important ones are set to zero, enabling significant compression. However, this method excludes dense layers, which typically contain more personalized information, from compression to preserve model accuracy. While this selective compression reduces overhead, it limits the overall efficiency gains, as the large compression matrices for non-dense layers significantly increase memory consumption on resource-limited clients, making it challenging to balance the need for efficient processing with constrained resources.

Moreover, numerical overflow during quantization can deviate model performance from convergence, as improperly scaled or shifted values may lead to inaccurate gradient updates and hinder effective model training. Gradient pruning is another approach to reduce the computational complexity during training in FL. This technique eliminates communication redundancy and minimizes storage and inference time, thus enhancing efficiency in distributed systems [[38]](#ref-38).

In this paper, we propose a novel method called QuanCrypt-FL, designed for application development in distributed machine learning (e.g., FL). Our study is divided into three phases. First, we integrate a robust FHE scheme (e.g., CKKS) to mitigate vulnerabilities arising from attacks, such as MIA and GI attacks, during both the training and inference phases. In contrast to BatchCrypt, our approach involves encrypting the full model update layer-wise from the local client device, which significantly reduces the training time compared to BatchCrypt. Second, to address the high computational complexity of HE in FL, we implement a low-bit quantization technique to reduce upload costs for users or organizations, although this introduces challenges related to numerical overflows. To address these challenges, we propose a mean-based dynamic layerwise clipping technique. Finally, we incorporate unstructured pruning to deactivate less important neurons during the upload of local models and the download of global models, thereby reducing the number of floating-point operations (FLOPs). Together, these techniques aim to minimize storage requirements and inference time. Additionally, quantization and pruning help reduce security vulnerabilities, even if a client is compromised by attackers, as the sparsified model limits their ability to infer sensitive information from the global model. Gradient pruning, introduced by Zhu *et al.* [[8]](#ref-8), reduces small-magnitude gradients to zero, significantly mitigating the impact of Gradient Inversion Attacks (GIA). Pruning over 70% of the gradients renders recovered images unrecognizable [[8]](#ref-8), [[39]](#ref-39), providing an additional layer of protection even in scenarios where edge clients are compromised. However, existing techniques have not fully addressed the vulnerabilities arising from the compromise of client models during HE implementation. As part of this, we conducted a well-known GIA attack on our decrypted global model to demonstrate the robustness of our method. To the best of our knowledge, this is the first time quantization and pruning are being implemented alongside FHE in FL. We successfully resolved inconsistencies related to the quantization process in our mechanism while maintaining the performance of the global model. By implementing a novel clipping technique to limit extreme values in the model updates before applying quantization, we ensured more stable and accurate results, leading to improved robustness of the model. The main contributions of this paper are provided below:

* We propose the efficient **QuanCrypt-FL mechanism**, which ensures robust privacy protection and resilience against inference attacks while minimizing computational complexity and reducing the impact on global model performance. We apply FHE layer-wise to client model updates, securing them against inference attacks. Further, we employ quantization and pruning to reduce communication and computation overhead. Specifically, pruning enhances efficiency while simultaneously providing resilience against adversarial threats, such as Gradient Inversion Attacks (GIA). Even with a decrypted model from clients or servers, an attacker will not be able to infer information by analyzing gradient. We provide practical defense guarantees by simulating a GIA on the final global model to demonstrate the effectiveness of our method in defending against such attacks.
* We integrate low-bit **quantization** and dynamic **pruning** with **HE** to enhance both efficiency and privacy. Quantization reduces the precision of model weights, resulting in a 3X reduction in storage usage. Pruning eliminates less important weights, further reducing aggregation costs and memory overhead. This combination optimizes the training process, achieving a 2X reduction in inference time compared to Vanilla FL and a 1.5X reduction

compared to BatchCrypt, by minimizing parameters and computational complexity.

* We propose a layerwise dynamic **mean-based clipping mechanism** to address numerical inconsistencies during the quantization process. This technique clips each layer's parameters based on their individual mean values, ensuring more precise handling of different weight distributions and improving stability and accuracy in the quantized model.
* We conduct **extensive empirical simulations** on the MNIST, CIFAR-10, and CIFAR-100 datasets, demonstrating significant improvements in model accuracy, storage efficiency, encryption time, decryption time, inference time, and training time compared to **BatchCrypt** [[30]](#ref-30) a privacy-preserving mechanisms.

The remainder of this paper is structured as follows: Section II outlines the current state-of-the-art studies in related works. Section III introduces the overview of threat model with mathematical analysis. Section IV outlines the methodology, which includes the QuanCrypt-FL algorithm. Section V presents the experiments and analyzes the results, followed by Section VI, which presents a detailed discussion and assessment. Finally, Section VII provides the conclusion and future works of the paper.

## II. Background and Related Work

In this section, we highlight the privacy requirements in FL and survey existing techniques, including Differential Privacy (DP), Secure Multiparty Computation (SMC), and HE. We explore the challenges of applying machine learning to homomorphically encrypted models and how efficiently HE enhances security against an honest-but-curious server and external adversaries.

The concept of DP [[40]](#ref-40), [[41]](#ref-41) has emerged as a crucial framework for providing quantifiable guarantees against data leakage. In FL, DP can be classified into two categories: Central Differential Privacy (CDP) and Local Differential Privacy (LDP). CDP ensures that the aggregate model does not reveal a client's participation or any information about individual training samples [[42]](#ref-42)–[[44]](#ref-44). LDP overcomes CDP limitations by ensuring privacy without trusting the data curator. In LDP, clients individually perturb or encode their data before submitting it to the central server [[45]](#ref-45)–[[47]](#ref-47). This approach helps obscure sensitive information by introducing noise to the model parameters. However, the primary drawback of DP is that this noise can degrade the performance of the global model [[48]](#ref-48). The trade-off between utility and noise is a key challenge of DP, making it impractical for real-time applications. This is especially problematic in scenarios where high precision and responsiveness are critical, such as in healthcare or autonomous driving applications, where even small accuracy losses caused by noise can lead to dangerous outcomes.

SMC is an effective method to protect model parameters from potential attacks in FL. It allows participants to contribute their data for computation without disclosing it to others [[49]](#ref-49). SMC has been implemented in FL to securely aggregate model parameters using privacy-preserving protocols [[50]](#ref-50), [[51]](#ref-51). However, SMC introduces high communication overhead and remains vulnerable to inference attacks, as the final output can still leak information about individual inputs [[52]](#ref-52). Additionally, client dropouts in SMC lead to delays, reduced system robustness, and incomplete model updates. In FL, SMC protocols can be adapted to handle client dropouts by using redundancy and failover mechanisms, ensuring continued training by redistributing tasks to active clients. This improves model robustness, as adaptive client scheduling and reliability selection further mitigate the negative effects of dropouts [[53]](#ref-53), [[54]](#ref-54).

HE has emerged as an important technique in FL for preserving data privacy by enabling computations on encrypted data without revealing sensitive information. Despite its security advantages, HE often leads to increased computational and communication overhead, necessitating optimization strategies to maintain efficiency [[55]](#ref-55)–[[57]](#ref-57). FPGA hardware accelerators technique, as demonstrated by Yang *et al.* [[58]](#ref-58), offer significant improvements in HE efficiency within FL systems. However, they did not provide an in-depth empirical analysis considering large-scale datasets and models. Other methods, such as the PFMLP framework [[26]](#ref-26) and the FastECDLP algorithm [[59]](#ref-59) are significant advancements in homomorphic encryption and elliptic curve-based systems, respectively. However, both present certain limitations. The PFMLP framework faces performance overhead due to homomorphic encryption operations, including communication overhead during training, encryption and decryption key length, and key replacement frequency, which can affect training efficiency. Conversely, while the FastECDLP algorithm significantly improves decryption efficiency in EC-based AHE schemes, it provides limited insights into its effect on encryption performance and scalability for longer plaintexts. Furthermore, there is minimal discussion on potential security implications for encryption within this context. The FedML-HE [[16]](#ref-16) system offers selective parameter encryption to reduce overheads, though it still faces challenges when scaling to more extensive models.

To further mitigate the overhead of HE in FL, quantization and sparsification techniques have been employed. BatchCrypt [[30]](#ref-30) and similar methods encode quantized gradients into compact representations, reducing encryption and communication costs while maintaining accuracy in cross-silo FL settings. However, these approaches can struggle to scale efficiently with larger deep learning models due to increased overhead. Zhu *et al.*'s [[60]](#ref-60) distributed additive encryption combined with quantization provides a notable reduction in computational demands by focusing on key parameters rather than encrypting the entire model. Techniques like DAEQ-FL enhance privacy in FL using additive ElGamal encryption and ternary quantization, but they face challenges in scaling to larger models due to the limited precision of ternary quantization, which can result in reduced accuracy for complex models [[60]](#ref-60). Sparsification techniques, such as those used in the FLASHE [[36]](#ref-36) scheme and Ma *et al.*'s [[25]](#ref-25) xMK-CKKS protocol, further enhance efficiency by reducing data volume and supporting modular operations, which involve performing computations within a fixed numerical range, thereby ensuring encryption consistency. This approach not only leads to lower communication costs but also improves computational performance. Despite these advancements, challenges remain in the deployment of HE in FL, primarily due to vulnerabilities to honest-but-curious clients and servers, as well as the inherent computational and communication bottlenecks during model training. While HE provides strong post-quantum security and preserves model performance by avoiding artificial noise and trusted environments, it still requires significant computational resources, especially in large-scale scenarios [[59]](#ref-59), [[61]](#ref-61).

To summarize, each privacy-preserving technique in FL has its own strengths and limitations. SMC provides strong privacy by enabling secure data aggregation without revealing individual contributions, but it incurs high communication overhead and is vulnerable to inference attacks, especially with client dropouts. DP is straightforward to implement, but its addition of noise can degrade model accuracy, limiting its use in precision-critical tasks. HE offers robust privacy by allowing computations on encrypted data without compromising accuracy or requiring major algorithm changes. Although its computational and communication overheads have traditionally hindered its scalability for large-scale deployments, ongoing advancements in optimization techniques and hardware acceleration are addressing these challenges, making HE increasingly viable for real-time applications. One notable advancement is the use of quantization techniques, which reduce the precision of encrypted data to minimize communication costs while maintaining accuracy. Another key improvement is the introduction of hardware acceleration with GPUs and FPGAs, significantly boosting the performance of HE computations by offloading intensive operations, such as modular arithmetic, onto specialized hardware. In conclusion, the choice of privacy-preserving technique in FL must consider the specific use case, as trade-offs between privacy, performance, and scalability are critical. Techniques like quantization combined with model pruning or sparsification in the FHE process can significantly reduce communication, storage, and training costs, all while maintaining performance integrity in both cross-silo and cross-device applications.

## III. Threat Model

In our mechanism, we assess the security of our method under two distinct adversarial scenarios. In the first scenario, the adversary has no knowledge of the model architecture, training parameters, or the underlying FL protocol. HE ensures that all communications between clients and the server remain fully encrypted, preventing the extraction of meaningful information even if encrypted model weights or parameters are intercepted, making this the strongest security assumption. In the second scenario, HE is applied, but the adversary gains access to decrypted model parameters or weights by compromising one or more participants, including honest but curious servers attempting to infer information. This simulates a more realistic threat model where adversaries leverage decrypted model parameters to infer sensitive data. To mitigate this, our framework employs pruning during FL, which significantly limits the adversary's ability to reconstruct raw client data or infer sensitive information, even when partial or full access to decrypted parameters or weights.

### A. Overview of Threat Model

FL has gained significant attention in both industry and academia due to its ability to train a global model across localized training data from multiple participants. However, this collaborative approach to machine learning is not without its vulnerabilities. MIA has been identified as a serious privacy concern in FL [[6]](#ref-6). These attacks involve adversaries training classification models to determine if a data record is part of the model's training dataset, potentially leading to privacy breaches [[6]](#ref-6). Unlike MIA, which aim to infer whether a specific data point was included in the training set, GIA [[62]](#ref-62) go a step further by reconstructing the actual training data from the gradients exchanged during model updates. While MIA threatens privacy by revealing membership information, GIA poses a more direct risk by recovering sensitive input data, such as images or personal information. One specific type of inference attack is the user-level inference attack, which targets individual users participating in FL [[63]](#ref-63). Additionally, local model reconstruction attacks have been studied, where adversaries eavesdrop on messages exchanged between clients and servers to reconstruct personalized models [[10]](#ref-10), [[64]](#ref-64).

### B. Mathematical Formulation

In this section, we focus on the security threats to FL, particularly on GIA [[10]](#ref-10). In a GIA, an adversary intercepts the gradients shared by clients with the central server and attempts to reconstruct the original input data by optimizing the difference in gradient directions. This optimization helps the adversary because the direction of the gradients provides information on how the model's parameters need to change to minimize the loss for specific input data. By iteratively adjusting a guessed input to align its gradient with that of the actual input, the adversary can gradually reconstruct the original data.

The adversary's goal can be formulated as an optimization problem. The equation below represents the objective for reconstructing client data by minimizing the cosine similarity between gradients. Cosine similarity is used because it measures the alignment of gradient directions, making it an ideal metric for determining how closely the reconstructed gradients match the actual ones, which helps refine the reconstruction process.

$$
\arg\min_{x\in[0,1]^n} \left(1 - \frac{\langle \nabla_{\theta} L_{\theta}(x,y), \nabla_{\theta} L_{\theta}(x^*,y) \rangle}{\|\nabla_{\theta} L_{\theta}(x,y)\| \|\nabla_{\theta} L_{\theta}(x^*,y)\|}\right) + \alpha \cdot \text{TV}(x) \tag{1}
$$

In Equation [1](#ref-1), the gradient of the loss function with respect to the model parameters for input, denoted as ∇(*theta*)L(*theta*)(x,y), is compared to the gradient for the ground truth input x*, ∇(*theta*)L(*theta*)(x*,y). The objective focuses on aligning the gradient directions rather than their magnitudes, as the direction of the gradient provides crucial information about how the model's predictions change in response to specific input data. By aligning the gradient directions, the adversary ensures that the reconstructed input leads to similar changes in the model's loss function as the original input, making the reconstruction more accurate. The gradient magnitudes, on the other hand, primarily reflect how far the model is from optimality, which can vary during training and does not contribute significantly to reconstructing the input. To preserve image smoothness, a regularization term *alpha* · TV(x), where TV(x) represents the total variation of the image, is included. Total Variation (TV) is commonly used in image reconstruction to reduce noise while preserving important edges in the image. By incorporating TV(x) in the optimization, the adversary ensures that the reconstructed image remains visually plausible, with reduced noise and preserved critical structures.

### C. Attack Practicality

Inference attacks, particularly gradient inversion attacks, have been demonstrated to pose significant and practical threats to FL systems. In these attacks, adversaries exploit the gradients or model updates exchanged between clients and the central server to reconstruct sensitive training data. Gradients are used to optimize model parameters by representing how much and in what direction the model's predictions should change with respect to the input data. However, this same process can unintentionally expose information about the underlying data because the gradients encode key features of the input, such as patterns or specific attributes that the model learns from. By analyzing these gradients, attackers can reverse-engineer and reconstruct the original input data, especially in models where the gradient directions reveal detailed information about the features that influence the model's predictions. This makes gradient inversion attacks both feasible and dangerous in real-world settings, as the gradients provide a rich source of data that adversaries can exploit. Connected autonomous vehicles (CAVs) can benefit from FL to allow for decentralized decision-making. CAV applications can be vulnerable to adversarial attacks during both the FL training and inference phases [[65]](#ref-65). FL allows AVs to improve models collaboratively by sharing aggregated model without exposing personal information. However, attacks like GIA and MIA still pose serious risks, as shared data may contain sensitive information about drivers, vehicle routes, and surroundings. For example, GIA could reconstruct images or AV sensor data collected during training, potentially revealing private information about pedestrians and drivers. These privacy threats are significant, as exposed data could disclose personal information or allow attackers to track specific vehicles by analyzing patterns.

Studies, such as *MiBench*, provide substantial evidence of this vulnerability by showing that even the partial extraction of gradient information can lead to the revelation of highly sensitive personal data, such as medical or financial records, in real-time environments [[66]](#ref-66). Gradients used for model optimization encode important features of the input data that are critical to the model's predictions. As a result, even small portions of gradient data can reveal patterns or attributes from the original dataset, which can be exploited by attackers to reconstruct sensitive information. This illustrates that these attacks are not merely theoretical but are actively being used to extract private information from models during deployment.

In another real-world example, adversaries used generative AI models to extract sensitive data from shared model outputs. In FL, the attack occurs when an adversary exploits the gradients shared by a victim during the training process to train a GAN (Generative Adversarial Network). The GAN's generator produces synthetic data that mimics the victim's private dataset, while the discriminator evaluates the quality based on the gradients. Over several iterations, the GAN learns to generate data closely resembling the victim's original data, allowing the attacker to reconstruct sensitive information and reverse-engineer the data distribution [[67]](#ref-67). This further underscores the practicality and danger of inference attacks, especially in large-scale FL deployments [[68]](#ref-68). These instances highlight the need for enhanced defenses like HE to protect FL systems from evolving threats. HE encrypts gradients during training, preventing adversaries and even the honest but curious server from accessing raw gradient data, thus preventing gradient inversion attacks. Additionally, gradient pruning limits the amount of gradient information exchanged, further reducing vulnerabilities. Together, these techniques significantly mitigate the risks of inference attacks during FL training and inference phase.

## IV. Methodology

In our proposed method, we implemented Homomorphic Encryption (HE) in FL with quantization and pruning to enhance training efficiency, reduce communication costs, and make the training process more resilient against inference attacks. QuanCrypt-FL framework is visualized in Figure [1](#fig-1).

The process begins by sharing the initial global model parameters **w**^0^ with all clients. Each client performs local training on its own dataset, followed by the aggregation of model updates at the server.

For each communication round *t*, the server first sends the current global model parameters **w**^t^ to each client *i*. The clients then perform local training using their respective datasets *D*~i~. During local training, each client computes the model update by minimizing the loss on its local dataset. The model update is calculated using the equation [2](#eq-2).

$$
\Delta \mathbf{w}_{i}^{t+1} = \mathbf{w}^{t} - \eta \nabla L(\mathbf{w}^{t}, D_{i}) \tag{2}
$$

where **w**^t^ are the global model parameters shared by the server at round *t*, Δ**w**^t+1^ represents the model update for client *i* after local training, *eta* is the learning rate used by the optimizer, and L(**w**^t^, *D*~i~) is the loss function evaluated on the local dataset *D*~i~.

During local model training, we employed a pruning technique to iteratively remove less important weights or gradients from the model updates. Specifically, clients perform soft, unstructured pruning based on the L1 norm, which creates a sparse model and makes the FL training process more efficient. The pruning process is guided by a dynamically updated pruning rate *p*~t~, which increases over the communication rounds, allowing for more aggressive pruning as training progresses. After pruning, clients send their pruned updates to the server,

<a id="fig-1"></a>![Overview of the proposed QuanCrypt-FL framework.](_page_5_Figure_0.jpeg)
<!-- Image Description: This flowchart illustrates a federated learning system with privacy-preserving model aggregation and pruning. Local clients perform encryption, quantization, clipping, and pruning on their model parameters before transmitting them to a central server. The server aggregates the encrypted parameters using FedAvg and performs server-side pruning. The process includes diagrams representing data transformation steps (encryption, quantization, clipping, pruning) and a flow depicting communication between clients and the server. The purpose is to detail the system's architecture for secure and efficient federated learning. -->

**Figure 1:** Overview of the proposed QuanCrypt-FL framework.

which aggregates them using FedAvg to generate the global model. This pruning technique not only reduces the model size and computational costs but also makes the training process more resistant to inference attacks.

By progressively increasing the pruning rate, the communication efficiency improves throughout the rounds. As clients share a sparsified model with the server, the transmitted model is no longer the full model, limiting the information available to potential attackers. The sparsity introduced by pruning constrains the parameter space, significantly reducing the chances of reverse engineering or inferring sensitive data. This reduction in exposed parameters inherently enhances privacy protection, making it more difficult for adversaries to extract meaningful insights about the underlying data. Weight pruning or sparsification process is visualized in Figure [2](#fig-2).

The pruning rate is updated iteratively using the equation [3](#eq-3).

$$
p_t = \max\left(0, \frac{t - t_{\text{eff}}}{t_{\text{target}} - t_{\text{eff}}}\right) \times \left(p_{\text{target}} - p_0\right) + p_0 \tag{3}
$$

where *p*~t~ is the pruning rate at round *t*, *t*~eff~ is the effective round when pruning starts, *t*~target~ is the target round when the target pruning rate is reached, *p*^0^ is the initial pruning rate, and *p*~target~ is the target pruning rate. This pruning rate increases gradually from the initial value to the target value, ensuring that pruning is progressively applied more aggressively as training advances.

Once pruning is applied to the model updates at each client, the pruned local model update Δ**w**^t+1^~p,i~, is computed as in equation [4](#eq-4).

$$
\Delta \mathbf{w}_{p,i}^{t+1} = \Delta \mathbf{w}_i^{t+1} \odot m_i^t \tag{4}
$$

where *odot* represents the element-wise product, and *m*^t^~i~ is the local pruning mask generated to identify which weights to

<a id="fig-2"></a>![Model sparsification using unstructured pruning based on L1 norm.](_page_5_Figure_10.jpeg)
<!-- Image Description: The image displays a weight matrix pruning process. Three 3x3 matrices are shown: an "Original Weight" matrix with floating-point values; a "Mask" matrix containing 0s and 1s; and a "Pruned Weight" matrix. The process involves applying the binary mask to the original weights, setting weights corresponding to 0s in the mask to near-zero, effectively pruning less important connections. The color-coding highlights the magnitude of the weights, with orange indicating the largest absolute value. -->

**Figure 2:** Model sparsification using unstructured pruning based on L1 norm.

prune at communication round *t*. This pruned update Δ**w**^t+1^~p,i~, is then quantized and sent to the server for aggregation.

<a id="alg-1"></a>**Algorithm 1:** Dynamic Mean-Based Clipping Technique

| Input: model update Δ*w*^t+1^~i~, clip factor *alpha* | | | | | | |
|---|---|---|---|---|---|---|
| Output: Clipped model update Δ*w*^t+1^~C,i~ | | | | | | |
| 1 foreach parameter Δ*w*^t+1^~i~ in the model update do | | | | | | |
| 2 if Δ*w*^t+1^~i~ is not floating-point then | | | | | | |
| 3 Convert Δ*w*^t+1^~i~ to floating-point | | | | | | |
| 4 end | | | | | | |
| 5 Compute *mu*~i~ = mean( Δ*w*^t+1^~i~ ) | | | | | | |
| 6 Δ*w*^t+1^~C,i~ *leftarrow* clip(Δ*w*^t+1^~i~, -*alpha* *cdot* *mu*~i~, *alpha* *cdot* *mu*~i~) | | | | | | |
| 7 end | | | | | | |
| 8 return Δ*w*^t+1^~C,i~ | | | | | | |

We also employed a dynamic mean-based layer-wise clipping technique in Algorithm [1](#alg-1) to help reduce inconsistencies during the training process. The clipping factor controls the clipping parameter, dynamically adjusting the clipping based on layer-wise updates, rather than using a static clipping method. This approach ensures that each layer's updates are clipped according to their specific dynamics, leading to more

<a id="fig-3"></a>![High Level Overview of the proposed QuanCrypt-FL mechanism.](_page_6_Figure_1.jpeg)
<!-- Image Description: The image is a flowchart depicting a federated learning algorithm. It illustrates a 15-step process, starting with sharing an initial global model and ending with saving the updated global model. Steps include local client training, pruning, parameter clipping and quantization, encryption, aggregation of encrypted parameters, and decryption for performance assessment. The flowchart visually represents the data flow and operations in each stage of the algorithm. -->

**Figure 3:** High Level Overview of the proposed QuanCrypt-FL mechanism.

stable and efficient training. After the local model updates are computed, each client clips its own model update Δ**w**^t+1^ to avoid instability before sending it to the server. The clipping for client *i*'s model update is applied using the following equation [5](#eq-5).

$$
\Delta \mathbf{w}_{\mathrm{C},i}^{t+1} = clip\left(\Delta \mathbf{w}_{i}^{t+1}, -\alpha \cdot \mu_{i}, \alpha \cdot \mu_{i}\right) \tag{5}
$$

where *mu*~i~ is the mean of the absolute values of the elements of client *i*'s model update, calculated as in equation [6](#eq-6).

$$
\mu_{i} = \frac{1}{n} \sum_{j=1}^{n} \left| \Delta \mathbf{w}_{i,j}^{t+1} \right| \tag{6}
$$

The clipping function *clip*(Δ**w**^t+1^, -*alpha* *cdot* *mu*~i~, *alpha* *cdot* *mu*~i~) ensures that the values of Δ**w**^t+1^ are constrained within the range [-*alpha* *cdot* *mu*~i~, *alpha* *cdot* *mu*~i~], limiting the impact of extreme values.

Next, each client performs quantization on the pruned and clipped model updates to reduce communication costs. The quantization process involves calculating the scaling factor and determining the quantized values to ensure the updates are compressed before transmission. The scaling factor is calculated using equation [7](#eq-7).

$$
s = \begin{cases} \frac{1.0}{q_{\text{max}} - q_{\text{min}}}, & \text{if } x_{\text{max}} = x_{\text{min}} = 0\\ \frac{x_{\text{min}}}{q_{\text{max}} - q_{\text{min}}}, & \text{if } x_{\text{max}} = x_{\text{min}} \neq 0\\ \frac{x_{\text{max}} - x_{\text{min}}}{q_{\text{max}} - q_{\text{min}}}, & \text{otherwise} \end{cases} \tag{7}
$$

Using this scaling factor *s*, the quantized values are then computed as in equation [8](#eq-8).

$$
q_x = round\left(\frac{x - x_{\text{min}}}{s} + z_0\right) \tag{8}
$$

where *z*^0^ represents the zero-point, calculated as:

*z*^0^ = *clip*(round(*x*~min~ - *q*~min~ *cdot* *s*), *q*~min~, *q*~max~)

The quantized values are then clamped to the range [*q*~min~, *q*~max~] and converted to the appropriate data type based on the bit width (e.g., 8-bit, 16-bit, or 32-bit) to minimize communication overhead.

After completing quantization, each client encrypts the quantized model updates using the CKKS homomorphic encryption scheme. The server then aggregates the encrypted updates from all clients using the following equation: *AggEnc*(Δ**w**) = (1/N) *sum*~i=1~^N^ *Enc*(Δ**w**^t+1^~q,i~, *H*).

Leveraging the homomorphic capabilities of CKKS, the server performs this aggregation directly on the encrypted model updates, without requiring decryption of individual updates. Since the server operates solely on ciphertexts, it can compute the sum of the encrypted updates element-wise while keeping each client's data private. This process ensures that even during aggregation, the server has no access to the underlying data. The resulting aggregated model remains encrypted and can be decrypted only by a trusted party or the clients, thus preserving data privacy throughout the FL training process. This approach aligns with the security and efficiency objectives of FL by enabling secure computations while safeguarding client data. After aggregation, the server decrypts the global model update to evaluate its performance using the following equation: Δ**w**^t+1^ = *Dec*(*AggEnc*(Δ**w**)). While the server can assess the overall model, individual client updates remain encrypted, ensuring privacy is preserved. This approach balances the need for performance evaluation with the protection of client data in the FL process.

The server then performs dequantization to recover the floating-point values using the following equation:

$$
x'=s\cdot (q_x-z_0).
$$

After the global model is updated and dequantized, pruning is applied to eliminate certain weights based on pruning rate. The pruned model weights **w**^t+1^~p~ are obtained by applying the pruning mask to the global model weights **w**^t+1^~dq~ as stated in here:

$$
w_p^{t+1} = w_{\rm dq}^{t+1} \odot m_t,
$$

where *odot* represents the element-wise (Hadamard) product, and *m*~t~ is the pruning mask applied to eliminate certain weights in the global model. Once pruning is applied to the global model, the pruned global model **w**^t+1^~p~ is sent to the clients for the next communication round. The clients will apply the same process again: local training, pruning, clipping, quantization, and secure aggregation. The pruning rate is updated iteratively for each round, and the process continues until the model converges. The final QuanCrypt-FL mechanism is presented in Algorithm [2](#alg-2). Moreover, step by step procedure of our method is depicted in Figure [3](#fig-3).

<a id="alg-2"></a>**Algorithm 2:** QuanCrypt-FL Mechanism

* **Input:** Global model **w**^0^, clients *N*, rounds *T*, learning rate *eta*, clip factor *alpha*, HE context *H*, quantization bit-length *bit*, initial pruning rate *p*^0^, target pruning rate *p*~target~, scaling factor *s*, zero-point *z*^0^, quantized weights Δ**w**~q~, dequantized weights Δ**w**~dq~, pruned weights **w**~p~
* **Output:** Trained global model **w**^T^
* **1 Init:** **w**^0^, *H*, client datasets, effective round *t*~eff~, target round *t*~target~
* **2 for** *each round* *t* = 1, . . . , *T* **do**
* **3 Server sends** **w**^t^ to all clients
* **4 for** each client *i* = 1,..., *N* **do**
* **5** Δ**w**^t+1^~i~ *leftarrow* **w**^t^ - *eta* *nabla* L(**w**^t^, *D*~i~)
* **6** *p*~t~ *leftarrow* max(0, (*t* - *t*~eff~)/(*t*~target~ - *t*~eff~)) *times* (*p*~target~ - *p*^0^) + *p*^0^
* **7** *m*^t^~i~ *leftarrow* pruning_mask(Δ**w**^t+1^~i~, *p*~t~, L1_norm)
* **8** Δ**w**^t+1^~p,i~ *leftarrow* Δ**w**^t+1^~i~ *odot* *m*^t^~i~
* **9** Δ**w**^t+1^~C,i~ *leftarrow* clip(Δ**w**^t+1^~p,i~, -*alpha* *cdot* *mu*~i~, *alpha* *cdot* *mu*~i~)
* **10** *s* *leftarrow* *cases* { 1.0/(*q*~max~ - *q*~min~), & *x*~max~ = *x*~min~ = 0 \\ 1/(*q*~max~ - *q*~min~), & *x*~max~ = *x*~min~ *neq* 0 \\ (*x*~max~ - *x*~min~)/(*q*~max~ - *q*~min~), & otherwise }
* **11** *q*~x~ *leftarrow* round((Δ**w**^t+1^~C,i~ - *x*~min~)/s + *z*^0^)
* **12** *q*~x~ *leftarrow* clip(*q*~x~, *q*~min~, *q*~max~)
* **13** Δ**w**^t+1^~q,i~ *leftarrow* Enc(*q*~x~, *H*)
* **14 end**
* **15** **w**^t+1^~q,g~ *leftarrow* (1/N) *sum*~i=1~^N^ Δ**w**^t+1^~q,i~
* **16** **w**^t+1^~dq~ *leftarrow* Dec(**w**^t+1^~q,g~, *H*)
* **17** *m*~t~ *leftarrow* pruning_mask(**w**^t+1^~dq~, *p*~t~, L1_norm)
* **18** **w**^t+1^~p~ *leftarrow* **w**^t+1^~dq~ *odot* *m*~t~
* **19 Server sends** **w**^t+1^~p~ to all clients
* **20 end**
* **21 return** **w**^T^

## V. Experiments and Result Analysis

### A. Experimental Setup

Our experiments were conducted on an Ubuntu server equipped with two NVIDIA RTX A6000 GPUs, an Intel Core i9 processor, and 128 GB of RAM. We explored FL across 10 to 50 clients using both IID and non-IID data distribution strategies. Each client independently trained their local models on a subset of data, using the Adam optimizer with a learning rate of 0.001 and a weight decay of 0.0001. Batch sizes were set at 64, or 128 depending on the number of clients, and each client trained for one local epoch per communication round. To ensure data privacy and security, we implemented HE with TenSEAL [[69]](#ref-69), based on Microsoft SEAL, adopting the CKKS scheme with a polynomial modulus degree of 16384 and coefficient modulus sizes [60, 40, 40, 40, 60]. The encryption context contained a public and private key pair shared among all clients, with the server using only the public key to securely aggregate model updates without revealing individual client data. For evaluation, model weights were decrypted with the private key.

### B. Datasets and Models

In our FL experiments, we used three datasets: CIFAR10 [[70]](#ref-70), CIFAR100 [[70]](#ref-70), and MNIST [[71]](#ref-71). These datasets were partitioned among clients using both IID and non-IID strategies to simulate different real-world data distribution scenarios. In the IID setting, data was evenly and randomly distributed among clients, whereas in the non-IID setting, each client received data containing only a subset of classes. CIFAR10 and CIFAR100 images were normalized using their respective mean and standard deviation values, while MNIST's grayscale images were normalized accordingly. The training datasets were split into 80% for training and 20% for validation, with each client receiving a portion for local training. For evaluation purposes, the full test dataset from each respective dataset (CIFAR10, CIFAR100, and MNIST) was used, ensuring that the model performance was assessed on a standardized and unchanged test set after each communication round.

Several models were utilized in the experiments, including CNN, AlexNet, and ResNet18, with each model trained locally on client data to evaluate performance under IID data distribution. The CNN is a CNN designed for MNIST dataset, consisting of two convolutional layers with ReLU activation, max-pooling, a fully connected layer, dropout, and an output layer. We modified AlexNet, adapted from the original AlexNet, includes four convolutional layers with 3x3 kernels, ReLU activations, maxpooling, dropout, two fully connected layers, and a softmax activation for classification. The ResNet18 model follows the standard ResNet-18 architecture, using BasicBlock to create four stages with increasing feature map sizes and downsampling, ending with average pooling and a fully connected output layer.

### C. Quantization and Pruning

In our FL experiments, we employed quantization to compress model updates, with the option to use 8-bit, 16-bit, or 32 bit quantization, controlled by the quantization bit-length *bit*, to reduce communication overhead. A clipping factor *alpha* = 3.0 was applied to manage extreme values in the model updates, ensuring stable training. For pruning, the initial pruning rate *p*^0^ was set to 20%, and pruning began at the effective round *t*~eff~ = 40. The pruning rate increased progressively until it reached the target pruning rate *p*~target~ = 50% by round *t*~target~ = 300. A pruning mask was applied to generate pruned weights **w**~p~, reducing the model size and computational cost while maintaining accuracy.

### D. Clipping, Smoothing, and Checkpoints

To control the magnitude of model updates, we applied a clipping mechanism with a clip factor *alpha*, set by default to 3.0 after conducting a grid search within the range [1.0,5.0]. This ensured that extreme values in model updates were controlled, ensuring stability during training and preventing large deviations.

<a id="fig-4"></a>![Comparison of methods considering 10 clients, Model: CNN, Dataset: MNIST, alpha=3.0, lambda=1.0.](_page_8_Figure_1.jpeg)
<!-- Image Description: The image displays two line graphs comparing the test accuracy of three Federated Learning (FL) methods: BatchCrypt, QuanCrypt-FL, and Vanilla-FL, across epochs. The main graph shows the overall accuracy trend, while an inset graph zooms in on a section (epochs 200-300) to highlight finer details. The purpose is to visually demonstrate the comparative performance and stability of the different FL algorithms in terms of achieving high test accuracy. -->

**Figure 4:** Comparison of methods considering 10 clients, Model: CNN, Dataset: MNIST, *alpha*=3.0, *lambda*=1.0.

In our FL model, we also incorporated a global learning rate hyperparameter *lambda* to adjust the influence of new model updates. At each communication round, the initial global parameter vector **w**~t,init~ and the updated parameter vector **w**~t,final~ were combined according to the following update rule [[72]](#ref-72):

**w**^t+1^ = (1-*lambda*)**w**~t,init~ + *lambda***w**~t,final~

When *lambda* = 1, the equation reverts to the standard update without smoothing. A grid search over *lambda* *in* {0.1,0.2, . . . ,1} was performed to select the best value for optimizing the model's convergence.

To further enhance model performance, we implemented a checkpointing mechanism with a patience of five epochs. If the validation accuracy did not improve after five consecutive epochs, the model was reloaded from the last checkpoint, ensuring that the model did not overfit or degrade in performance during training.

### E. Result Analysis

We will provide a comparative analysis of our proposed method with BatchCrypt and Vanilla FL. The results will be evaluated across multiple metrics, including model accuracy, training time, encryption time, decryption time, inference time, and storage efficiency. This analysis will demonstrate the effectiveness of our approach in enhancing both computational performance and security in FL.

Figure [4](#fig-4) shows the test accuracy comparison of BatchCrypt, QuanCrypt-FL, and Vanilla-FL on the MNIST dataset using a CNN model with 10 clients over 300 communication rounds. The results indicate that BatchCrypt starts with reasonably high accuracy but quickly stabilizes at around 99.04%, consistently underperforming compared to both QuanCrypt-FL and Vanilla-FL. QuanCrypt-FL, however, closely tracks Vanilla-FL throughout the training, reaching an accuracy of 99.40% by the final round, while Vanilla-FL achieves a similar result of 99.32%. This minimal difference between QuanCrypt-FL and Vanilla-FL demonstrates that QuanCrypt-FL achieves nearly identical performance to Vanilla-FL, while offering additional privacy-preserving features. BatchCrypt, although competitive, lags behind both methods across all 300 rounds, showing the trade-offs involved in using a heavier encryption mechanism. Ultimately, QuanCrypt-FL maintains strong accuracy

![Comparison of Methods for several clients, Model: CNN, Dataset: MNIST, alpha=3.0, lambda=1.0.](_page_8_Figure_10.jpeg)
<!-- Image Description: The bar chart displays the maximum accuracy achieved by three Federated Learning (FL) methods (BatchCrypt, QuanCrypt-FL, Vanilla FL) across varying numbers of clients (10, 20, 30, 40, 50). Each bar represents the maximum accuracy for a given method and client count. The chart illustrates the performance comparison of these methods, showing how accuracy changes with the number of participating clients. Accuracy values are close to 99% in all cases. -->

**Figure 5:** Comparison of Methods for several clients, Model: CNN, Dataset: MNIST, *alpha*=3.0, *lambda*=1.0.

comparable to Vanilla-FL and clearly outperforms BatchCrypt, making it a more effective choice when both privacy and accuracy are essential.

Figure [5](#fig-5) illustrates the maximum accuracy achieved by BatchCrypt, QuanCrypt-FL, and Vanilla-FL across different client counts (10, 20, 30, 40, 50) on the MNIST dataset using a CNN model. QuanCrypt-FL consistently performs at the highest level, achieving 99.44% for 10 clients, slightly outperforming Vanilla-FL at 99.40%. As the number of clients increases, QuanCrypt-FL maintains strong accuracy with 99.29% for 20 clients, 99.22% for 30 clients, 99.10% for 40 clients, and 98.98% for 50 clients. Vanilla-FL closely follows with accuracies of 99.33%, 99.20%, 99.06%, and 98.97% for the same client counts, respectively. In contrast, BatchCrypt consistently underperforms compared to both QuanCrypt-FL and Vanilla-FL, reaching 99.14% for 10 clients and showing slightly lower values for the remaining client counts, with accuracies ranging between 99.00% and 99.13%. While BatchCrypt provides competitive results, it consistently lags behind the higher performance of QuanCrypt-FL and Vanilla-FL, demonstrating the superior ability of QuanCrypt-FL to maintain high accuracy while incorporating privacy-preserving features.

A comparison of BatchCrypt, QuanCrypt-FL, and Vanilla-FL on the CIFAR-10 dataset with 10 clients reveals key differences in performance, as shown in Figure [6](#fig-6). While BatchCrypt initially achieves slightly higher accuracy in the early rounds, it quickly falls behind as training progresses. By the final epochs, QuanCrypt-FL and Vanilla-FL reach similar accuracy levels of approximately 80.40%, whereas BatchCrypt lags significantly with a final accuracy of 69.96%. This substantial performance differ of over 10.00% underscores the trade-offs inherent in BatchCrypt, where the pursuit of privacy leads to a notable compromise in accuracy. On the other hand, QuanCrypt-FL closely matches the performance of Vanilla-FL, demonstrating its ability to maintain accuracy while offering including privacy features.

In the case of 50 clients, the differences in performance between BatchCrypt, QuanCrypt-FL, and Vanilla-FL become even more pronounced, as shown in Figure [7](#fig-7). While BatchCrypt initially shows some promise in the early rounds, it fails to keep up as training progresses. By the final epochs, QuanCrypt-FL achieves an accuracy of 73.12%, closely aligning with Vanilla-FL's 75.90%, while BatchCrypt trails behind with 66.85%. This (7-9)% difference further highlights BatchCrypt's limitations in scaling effectively. In contrast, QuanCrypt-FL consistently maintains competitive accuracy, making it a reliable and scalable choice for FL scenarios with larger client bases.

Figure [8](#fig-8) compares the performance of BatchCrypt, QuanCrypt-FL, and Vanilla-FL on the CIFAR-10 dataset using the AlexNet model, with the x-axis representing the number of clients (10, 20, 30, 40, 50) and the y-axis showing the maximum accuracy achieved over 300 communication rounds. QuanCrypt-FL consistently achieves accuracy close to Vanilla-FL across all client counts. For example, at 10 clients, QuanCrypt-FL achieves an accuracy of 81.45%, which is almost identical to Vanilla-FL's 81.64%. As the number of clients increases, QuanCrypt-FL continues to perform strongly, reaching accuracies of 79.62%, 78.96%, 77.10%, and 75.62% for 20, 30, 40, and 50 clients, respectively. In contrast, BatchCrypt shows a noticeable drop in performance, with accuracies starting at 70.84% for 10 clients and steadily declining to 68.18% at 50 clients. While Vanilla-FL remains the top performer with accuracies of 81.64%, 80.39%, 80.29%, 78.92%, and 78.05% as the client count increases, the minimal difference between QuanCrypt-FL and Vanilla-FL indicates that QuanCrypt-FL closely approximates Vanilla-FL's performance while consistently outperforming BatchCrypt across all client counts.

Due to space limitations, we do not provide the result visualization of the CIFAR-100 dataset. Table [I](#tbl-1) presents the comparative analysis results for all methods across different datasets and models, including CIFAR-10 using AlexNet and CIFAR-100 using AlexNet and ResNet18. The results demonstrate that QuanCrypt-FL outperforms BatchCrypt. For CIFAR-10, we achieve accuracy similar to Vanilla FL, with less than a 1% accuracy loss, while BatchCrypt shows a greater than 10% accuracy loss compared to Vanilla FL across different client counts (10, 20, 30, 40, 50). For the CIFAR-100 dataset with the AlexNet model, QuanCrypt-FL achieves accuracy close to Vanilla FL, except for an approximate 5% loss for 20 clients, whereas BatchCrypt exhibits a greater than 15% accuracy loss. For the ResNet18 model on CIFAR-100, Vanilla FL achieves around 54% accuracy, while QuanCrypt-FL reaches approximately 50%, and BatchCrypt experiences a 20% accuracy loss compared to Vanilla FL.

Figure [9](#fig-9) presents the comparison between BatchCrypt and QuanCrypt-FL in terms of encryption time, decryption time, average inference time, and training time, as the number of clients increases (10, 20, 30, 40, 50). The results reveal significant differences in performance with the existing methods, with QuanCrypt-FL demonstrating considerable time efficiency across all metrics.

For **encryption time**, BatchCrypt consistently requires more time as the number of clients increases, ranging from 8.97 hours at 10 clients to 10.07 hours at 50 clients. In contrast, QuanCrypt-FL shows much shorter encryption times, ranging from 0.97 hours at 10 clients to 4.90 hours at 50 clients. This indicates that QuanCrypt-FL is **up to 9 times faster** than BatchCrypt in encryption time, particularly as the number of clients grows.

In terms of **decryption time**, BatchCrypt decreases its time from 23.55 minutes at 10 clients to 10.66 minutes at 50 clients. However, QuanCrypt-FL maintains a much more efficient and stable decryption time, ranging from 1.42 minutes at 10 clients to 1.45 minutes at 50 clients, making it **up to 16 times faster** than BatchCrypt.

When comparing **average inference time**, BatchCrypt stays relatively stable, with values around 2.02 seconds, whereas QuanCrypt-FL achieves faster inference times, ranging from 1.30 to 1.34 seconds. This demonstrates that QuanCrypt-FL is **about 1.5 times faster** in inference compared to BatchCrypt.

Finally, for **training time**, BatchCrypt requires between 16.60 and 17.59 hours as the client count increases, while QuanCrypt-FL significantly reduces training time, from 1.83 hours at 10 clients to 5.86 hours at 50 clients. This makes QuanCrypt-FL **up to 3 times faster** in training compared to BatchCrypt.

In terms of storage, we calculate communication costs for model uploads as shown in Figure [10](#fig-10). During uploads, we apply quantization to compress model parameters into an 8 bit format, significantly reducing upload costs. For downloads, clients typically receive the full model in a 32-bit format, which increases communication costs. To address this, pruning can be considered an effective approach to reduce costs. Although our mechanism currently uses a 32-bit format for download costs, pruning can reduce costs by setting less important weights to zero after aggregation and encoding sparse parameters in a 4-bit format, while retaining non-sparse parameters in 32-bit format. While we applied pruning, we did not visualize the download cost in our results. This approach effectively reduces both upload and potential download costs while preserving model performance.

We simulated a Gradient Inversion Attack (GIA) on both our proposed QuanCrypt-FL model and the Vanilla FL model. For the attack simulation, we used 10 clients and a ResNet18 model and CIFAR10 dataset in both methods. Apart from enhancing efficiency, pruning is also employed as a defense mechanism against attacks in our approach. By reducing the model's complexity through pruning, we introduce sparsity, which limits the success of attacks like GIA. This dual benefit of pruning not only improves computational performance but also strengthens the model's resistance to adversarial attacks, ensuring greater security during the training process. Specifically, we set the initial pruning rate at 30% and progressively increased it to a target pruning rate of 70%.

In Figure [11](#fig-11), subfigures (a) original images, while subfigure (b) shows the reconstructed image generated by the GIA attack in Vanilla FL, as described in the threat model section. In Vanilla FL, the attack was nearly 100% successful in reconstructing the original image from the gradients. However, in our QuanCrypt-FL method, due to the sparsity introduced by the pruning technique, the GIA was unsuccessful in reconstructing the original image from the gradients in figure (c).

This demonstrates that, even if the server or adversary has access to the shared model parameters, it cannot infer sensitive information or reconstruct data from the shared gradients or even from the decrypted global model used for inference and

<a id="fig-6"></a>![Comparison of accuracy considering 10 clients, Model: AlexNet, Dataset: CIFAR10, alpha=3.0, lambda=1.0.](_page_10_Figure_1.jpeg)
<!-- Image Description: The image displays a line graph comparing the test accuracy of three Federated Learning (FL) methods: BatchCrypt, QuanCrypt-FL, and Vanilla-FL, over 300 epochs. The main graph shows overall accuracy trends. A zoomed-in inset graph details accuracy fluctuations between epochs 150 and 300 for QuanCrypt-FL and Vanilla-FL, highlighting performance variations during later training stages. The purpose is to visually compare the convergence and stability of the different FL algorithms. -->

**Figure 6:** Comparison of accuracy considering 10 clients, Model: AlexNet, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0.

![Comparison of accuracy considering 50 clients, Model: AlexNet, Dataset: CIFAR10, alpha=3.0, lambda=1.0.](_page_10_Figure_3.jpeg)
<!-- Image Description: The image displays a line graph comparing the test accuracy of three Federated Learning (FL) methods: BatchCrypt, QuanCrypt-FL, and Vanilla-FL, across 300 epochs. The x-axis represents the number of epochs, and the y-axis shows the test accuracy. The graph illustrates the performance of each method over time, allowing for a comparison of their convergence and final accuracy. The purpose is to demonstrate the relative effectiveness of the different FL approaches in achieving high accuracy. -->

**Figure 7:** Comparison of accuracy considering 50 clients, Model: AlexNet, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0.

<a id="fig-8"></a>![Comparison of HE mechanism, Model: AlexNet, Dataset: CIFAR10, alpha=3.0, lambda=1.0.](_page_10_Figure_5.jpeg)
<!-- Image Description: The image displays a bar chart comparing the maximum accuracy of three federated learning methods (BatchCrypt, QuanCrypt-FL, Vanilla FL) across varying numbers of clients (10, 20, 30, 40, 50). Each bar represents a method's accuracy for a given client count. The chart's purpose is to visually demonstrate and compare the performance of these methods under different client-participation scenarios. Numerical accuracy values are shown atop each bar. -->

**Figure 8:** Comparison of HE mechanism, Model: AlexNet, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0.

<a id="fig-9"></a>![Comparison of time of HE mechanism, Model: AlexNet, Dataset: CIFAR10, alpha=3.0, lambda=1.0.](_page_10_Figure_7.jpeg)
<!-- Image Description: This image presents four line graphs comparing the performance of BatchCrypt and QuanCrypt-FL methods across varying numbers of clients (10-50). The graphs display encryption time (hours), decryption time (minutes), average inference time (seconds), and training time (hours) for each method. The purpose is to illustrate the scalability and efficiency differences between the two cryptographic approaches in a federated learning context. BatchCrypt shows generally lower latency except for training time which is significantly higher than QuanCrypt-FL. -->

**Figure 9:** Comparison of time of HE mechanism, Model: AlexNet, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0.

<a id="tbl-1"></a>**TABLE I:** Comparative performance analysis.

| Method | Model | Dataset | Number of Clients | Maximum Test Acc |
|---|---|---|---|---|
| BatchCrypt | AlexNet | CIFAR-10 | 10 | 70.84% |
| | | | 20 | 69.54% |
| | | | 30 | 67.21% |
| | | | 40 | 70.15% |
| | | | 50 | 68.18% |
| QuanCrypt-FL | AlexNet | CIFAR-10 | 10 | 81.45% |
| | | | 20 | 79.62% |
| | | | 30 | 78.96% |
| | | | 40 | 77.10% |
| | | | 50 | 75.62% |
| Vanilla-FL | AlexNet | CIFAR-10 | 10 | 81.64% |
| | | | 20 | 80.39% |
| | | | 30 | 80.29% |
| | | | 40 | 78.92% |
| | | | 50 | 78.05% |
| BatchCrypt | AlexNet | CIFAR-100 | 10 | 34.58% |
| | | | 20 | 33.14% |
| | | | 30 | 33.56% |
| | | | 40 | 32.87% |
| | | | 50 | 33.73% |
| QuanCrypt-FL | AlexNet | CIFAR-100 | 10 | 47.90% |
| | | | 20 | 43.70% |
| | | | 30 | 48.81% |
| | | | 40 | 48.62% |
| | | | 50 | 45.40% |
| Vanilla-FL | AlexNet | CIFAR-100 | 10 | 48.59% |
| | | | 20 | 49.54% |
| | | | 30 | 49.14% |
| | | | 40 | 48.93% |
| | | | 50 | 49.68% |
| BatchCrypt | ResNet18 | CIFAR-100 | 10 | 34.05% |
| | | | 20 | 33.14% |
| | | | 30 | 35.74% |
| | | | 40 | 36.56% |
| | | | 50 | 33.73% |
| QuanCrypt-FL | ResNet18 | CIFAR-100 | 10 | 48.21% |
| | | | 20 | 48.89% |
| | | | 30 | 48.66% |
| | | | 40 | 49.26% |
| | | | 50 | 48.70% |
| Vanilla-FL | ResNet18 | CIFAR-100 | 10 | 52.62% |
| | | | 20 | 53.48% |
| | | | 30 | 54.08% |
| | | | 40 | 53.90% |
| | | | 50 | 54.20% |

<a id="fig-10"></a>![Comparison of upload cost for different models, Dataset: CIFAR10, alpha=3.0, lambda=1.0.](_page_11_Figure_2.jpeg)
<!-- Image Description: This bar chart compares the upload costs (in GB) of three Convolutional Neural Networks (CNNs): CNN, AlexNet, and ResNet18. Two costs are shown for each model: the original upload cost and a quantized upload cost (presumably after model compression). The chart demonstrates a significant reduction in upload cost after quantization, especially for ResNet18, highlighting the effectiveness of the quantization technique. -->

**Figure 10:** Comparison of upload cost for different models, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0.

evaluation.

## VI. Discussion

Our proposed mechanism, QuanCrypt-FL, achieves state-of-the-art performance compared to existing methods that implement HE with pruning and quanization in FL. Compared to BatchCrypt's approach of batching quantized gradient values into smaller units, our layer-wise encryption strategy in FL significantly reduces the frequency of encryption and decryption operations required per training round. By encrypting entire layers instead of smaller gradient batches, we streamline the encryption process, resulting in faster overall FL training times. This approach also reduces computational overhead during aggregation, as each layer can be processed as a single encrypted unit, simplifying the update process. Consequently, our method enhances the efficiency and scalability of secure FL, making it a practical choice for applications prioritizing

<a id="fig-11"></a>![Comparison of image reconstruction using GIA, Model: ResNet18, Dataset: CIFAR10, alpha=3.0, lambda=1.0. (a) Original image, (b) Gradient inversion attack on the global model in Vanilla FL, (c) Gradient inversion attack on global model in QuanCrypt-FL](_page_11_Figure_7.jpeg)
<!-- Image Description: The image displays three low-resolution images (a, b, c) of an emu-like bird in a grassy field. Each image represents a different level of image degradation or compression, progressively losing detail from (a) to (c). The purpose is likely to illustrate the impact of image processing techniques or data loss on image quality within the context of the paper. -->

**Figure 11:** Comparison of image reconstruction using GIA, Model: ResNet18, Dataset: CIFAR10, *alpha*=3.0, *lambda*=1.0. (a) Original image, (b) Gradient inversion attack on the global model in Vanilla FL, (c) Gradient inversion attack on global model in QuanCrypt-FL

both speed and data privacy. We present a detailed comparative analysis with the BatchCrypt. While BatchCrypt can achieve similar accuracy to our method on simpler datasets like MNIST, it shows significant limitations with larger and more complex datasets such as CIFAR-100. For example, in our experiments using CIFAR-100 with the AlexNet model, BatchCrypt achieved very low accuracy, whereas our method reached accuracy levels close to Vanilla FL. In this setup, we used an IID data distribution and allocated 5000 data samples per client.

Moreover, we observed that BatchCrypt incurs considerably higher computational complexity compared to QuanCrypt-FL. We achieved faster encryption, decryption, inference, and training time. Moreover. our method requires less memory, reducing the upload cost for clients during FL training. Additionally, we implemented iterative pruning to create a progressively sparse model during the communication rounds, which reduces inference time. As a result, QuanCrypt-FL demonstrates faster inference speeds than both BatchCrypt and Vanilla FL. Furthermore, pruning also strengthens defenses against GIA; a semi-honest server or adversary cannot infer sensitive information, even with access to client model updates or the global model. If we increase the pruning rate beyond 70%, our defense technique becomes more resilient against GIA attacks under the adversarial scenario or in the case of an honest but curious server. However, we need to maintain a tradeoff between the pruning rate and utility to make our mechanism feasible for real-world scenarios.

## VII. Conclusion

In this paper, we propose QuanCrypt-FL, a novel FL method that employs low-bit quantization and pruning with layer-wise model encryption to enhance both security and efficiency in FL. QuanCrypt-FL effectively mitigates inference attacks, such as gradient inversion and membership inference, by encrypting model updates and reducing communication overhead through quantization and pruning. Although HE is computationally expensive, our evaluation demonstrates that QuanCrypt-FL significantly improves computational performance and privacy protection compared to existing methods, achieving faster encryption, decryption, inference, and training times while maintaining accuracy levels comparable to those of vanilla FL method. This approach is scalable for cross-silo and cross-device applications where both security and utility are essential. It offers a communication-efficient and privacy-preserving solution suitable for real-world applications. Future work could explore adaptive structured pruning to further enhance scalability and efficiency in larger FL deployments.

### Acknowledgement

This work is based upon the work supported by the National Center for Transportation Cybersecurity and Resiliency (TraCR) (a U.S. Department of Transportation National University Transportation Center) headquartered at Clemson University, Clemson, South Carolina, USA. Any opinions, findings, conclusions, and recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of TraCR, and the U.S. Government assumes no liability for the contents or use thereof.

### References

* <a id="ref-1"></a>[1] J. S. Baik, "Data privacy against innovation or against discrimination?: The case of the california consumer privacy act (ccpa)," *Telematics and Informatics*, vol. 52, 2020.
* <a id="ref-2"></a>[2] S. M. Boyne, "Data protection in the united states," *The American Journal of Comparative Law*, vol. 66, no. suppl_1, pp. 299–343, 2018.
* <a id="ref-3"></a>[3] M. Hintze, "Science and privacy: data protection laws and their impact on research," *Wash. JL Tech. & Arts*, vol. 14, p. 103, 2018.
* <a id="ref-4"></a>[4] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, "Communication-efficient learning of deep networks from decentralized data," in *Artificial intelligence and statistics*. PMLR, 2017, pp. 1273– 1282.
* <a id="ref-5"></a>[5] C. Huang, J. Huang, and X. Liu, "Cross-silo federated learning: Challenges and opportunities," *arXiv preprint arXiv:2206.12949*, 2022.
* <a id="ref-6"></a>[6] Y. Gu, Y. Bai, and S. Xu, "Cs-mia: Membership inference attack based on prediction confidence series in federated learning," *Journal of Information Security and Applications*, vol. 67, p. 103201, 2022.
* <a id="ref-7"></a>[7] Y. Gu, Y. Bai, and S. Xu, "Cs-mia: Membership inference attack based on prediction confidence series in federated learning," *Journal of Information Security and Applications*, vol. 67, p. 103201, 2022.
* <a id="ref-8"></a>[8] L. Zhu, Z. Liu, and S. Han, "Deep leakage from gradients," *Advances in neural information processing systems*, vol. 32, 2019.
* <a id="ref-9"></a>[9] B. Zhao, K. R. Mopuri, and H. Bilen, "idlg: Improved deep leakage from gradients," *arXiv preprint arXiv:2001.02610*, 2020.
* <a id="ref-10"></a>[10] J. Geiping, H. Bauermeister, H. Dröge, and M. Moeller, "Inverting gradients-how easy is it to break privacy in federated learning?" *Advances in neural information processing systems*, vol. 33, pp. 16 937– 16 947, 2020.
* <a id="ref-11"></a>[11] H. Liang, Y. Li, C. Zhang, X. Liu, and L. Zhu, "Egia: An external gradient inversion attack in federated learning," *IEEE Transactions on Information Forensics and Security*, 2023.
* <a id="ref-12"></a>[12] Z. Li, L. Wang, G. Chen, Z. Zhang, M. Shafiq, and Z. Gu, "E2egi: End-to-end gradient inversion in federated learning," *IEEE Journal of Biomedical and Health Informatics*, vol. 27, no. 2, pp. 756–767, 2022.
* <a id="ref-13"></a>[13] J. Xu, C. Hong, J. Huang, L. Y. Chen, and J. Decouchant, "Agic: Approximate gradient inversion attack on federated learning," in *2022 41st International Symposium on Reliable Distributed Systems (SRDS)*. IEEE, 2022, pp. 12–22.
* <a id="ref-14"></a>[14] J. Jeon, K. Lee, S. Oh, J. Ok *et al.*, "Gradient inversion with generative image prior," *Advances in neural information processing systems*, vol. 34, pp. 29 898–29 908, 2021.
* <a id="ref-15"></a>[15] O. Goldreich, *Foundations of cryptography: volume 2, basic applications*. Cambridge university press, 2001, vol. 2.
* <a id="ref-16"></a>[16] W. Jin, Y. Yao, S. Han, C. Joe-Wong, S. Ravi, S. Avestimehr, and C. He, "Fedml-he: An efficient homomorphic-encryption-based privacy-preserving federated learning system," *arXiv preprint arXiv:2303.10837*, 2023.
* <a id="ref-17"></a>[17] C. Hu and B. Li, "Maskcrypt: Federated learning with selective homomorphic encryption," *IEEE Transactions on Dependable and Secure Computing*, 2024.
* <a id="ref-18"></a>[18] E. Hosseini and A. Khisti, "Secure aggregation in federated learning via multiparty homomorphic encryption," in *2021 IEEE Globecom Workshops (GC Wkshps)*. IEEE, 2021, pp. 1–6.
* <a id="ref-19"></a>[19] M. Gong, Y. Zhang, Y. Gao, A. K. Qin, Y. Wu, S. Wang, and Y. Zhang, "A multi-modal vertical federated learning framework based on homomorphic encryption," *IEEE Transactions on Information Forensics and Security*, 2023.
* <a id="ref-20"></a>[20] T. ElGamal, "A public key cryptosystem and a signature scheme based on discrete logarithms," *IEEE transactions on information theory*, vol. 31, no. 4, pp. 469–472, 1985.
* <a id="ref-21"></a>[21] P. Paillier, "Public-key cryptosystems based on composite degree residuosity classes," in *International conference on the theory and applications of cryptographic techniques*. Springer, 1999, pp. 223–238.
* <a id="ref-22"></a>[22] D. Boneh, E.-J. Goh, and K. Nissim, "Evaluating 2-dnf formulas on ciphertexts," in *Theory of Cryptography: Second Theory of Cryptography Conference, TCC 2005, Cambridge, MA, USA, February 10-12, 2005. Proceedings 2*. Springer, 2005, pp. 325–341.
* <a id="ref-23"></a>[23] C. Gentry, *A fully homomorphic encryption scheme*. Stanford university, 2009.
* <a id="ref-24"></a>[24] Z. Brakerski and V. Vaikuntanathan, "Fully homomorphic encryption from ring-lwe and security for key dependent messages," in *Annual cryptology conference*. Springer, 2011, pp. 505–524.
* <a id="ref-25"></a>[25] J. Ma, S.-A. Naas, S. Sigg, and X. Lyu, "Privacy-preserving federated learning based on multi-key homomorphic encryption," *International Journal of Intelligent Systems*, vol. 37, no. 9, pp. 5880–5901, 2022.
* <a id="ref-26"></a>[26] H. Fang and Q. Qian, "Privacy preserving machine learning with homomorphic encryption and federated learning," *Future Internet*, vol. 13, no. 4, p. 94, 2021.
* <a id="ref-27"></a>[27] B. Wang, H. Li, Y. Guo, and J. Wang, "Ppflhe: A privacy-preserving federated learning scheme with homomorphic encryption for healthcare data," *Applied Soft Computing*, vol. 146, p. 110677, 2023.
* <a id="ref-28"></a>[28] W. Ou, J. Zeng, Z. Guo, W. Yan, D. Liu, and S. Fuentes, "A homomorphic-encryption-based vertical federated learning scheme for rick management," *Computer Science and Information Systems*, vol. 17, no. 3, pp. 819–834, 2020.
* <a id="ref-29"></a>[29] B. Jia, X. Zhang, J. Liu, Y. Zhang, K. Huang, and Y. Liang, "Blockchain-enabled federated learning data protection aggregation scheme with differential privacy and homomorphic encryption in iiot," *IEEE Transactions on Industrial Informatics*, vol. 18, no. 6, pp. 4049–4058, 2021.
* <a id="ref-30"></a>[30] C. Zhang, S. Li, J. Xia, W. Wang, F. Yan, and Y. Liu, "{BatchCrypt}: Efficient homomorphic encryption for {Cross-Silo} federated learning," in *2020 USENIX annual technical conference (USENIX ATC 20)*, 2020, pp. 493–506.
* <a id="ref-31"></a>[31] C. Liu, S. Chakraborty, and D. Verma, "Secure model fusion for distributed learning using partial homomorphic encryption," *Policy-Based Autonomic Data Governance*, pp. 154–179, 2019.
* <a id="ref-32"></a>[32] P. W. Shor, "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer," *SIAM review*, vol. 41, no. 2, pp. 303–332, 1999.
* <a id="ref-33"></a>[33] J. H. Cheon, A. Kim, M. Kim, and Y. Song, "Homomorphic encryption for arithmetic of approximate numbers," in *Advances in Cryptology– ASIACRYPT 2017: 23rd International Conference on the Theory and Applications of Cryptology and Information Security, Hong Kong, China, December 3-7, 2017, Proceedings, Part I 23*. Springer, 2017, pp. 409–437.
* <a id="ref-34"></a>[34] Z. Brakerski, C. Gentry, and V. Vaikuntanathan, "(leveled) fully homomorphic encryption without bootstrapping," *ACM Transactions on Computation Theory (TOCT)*, vol. 6, no. 3, pp. 1–36, 2014.
* <a id="ref-35"></a>[35] J. Fan and F. Vercauteren, "Somewhat practical fully homomorphic encryption," *Cryptology ePrint Archive*, 2012.
* <a id="ref-36"></a>[36] Z. Jiang, W. Wang, and Y. Liu, "Flashe: Additively symmetric homomorphic encryption for cross-silo federated learning," 2021.
* <a id="ref-37"></a>[37] W. Yang, Y. Bai, Y. Rao, H. Wu, G. Xing, and Y. Zhou, "Privacy-preserving federated learning with homomorphic encryption and sparse compression," in *2024 4th International Conference on Computer Communication and Artificial Intelligence (CCAI)*. IEEE, 2024, pp. 192– 198.
* <a id="ref-38"></a>[38] Q. Long, C. Anagnostopoulos, S. P. Parambath, and D. Bi, "Feddip: Federated learning with extreme dynamic pruning and incremental regularization," in *2023 IEEE International Conference on Data Mining (ICDM)*. IEEE, 2023, pp. 1187–1192.
* <a id="ref-39"></a>[39] Y. Huang, S. Gupta, Z. Song, K. Li, and S. Arora, "Evaluating gradient inversion attacks and defenses in federated learning," *Advances in neural information processing systems*, vol. 34, pp. 7232–7241, 2021.
* <a id="ref-40"></a>[40] C. Dwork, K. Kenthapadi, F. McSherry, I. Mironov, and M. Naor, "Our data, ourselves: Privacy via distributed noise generation," in *Advances in Cryptology-EUROCRYPT 2006: 24th Annual International Conference on the Theory and Applications of Cryptographic Techniques, St. Petersburg, Russia, May 28-June 1, 2006. Proceedings 25*. Springer, 2006, pp. 486–503.
* <a id="ref-41"></a>[41] C. Dwork, F. McSherry, K. Nissim, and A. Smith, "Calibrating noise to sensitivity in private data analysis," in *Theory of Cryptography: Third Theory of Cryptography Conference, TCC 2006, New York, NY, USA, March 4-7, 2006. Proceedings 3*. Springer, 2006, pp. 265–284.
* <a id="ref-42"></a>[42] C. Dwork, A. Roth *et al.*, "The algorithmic foundations of differential privacy," *Foundations and Trends® in Theoretical Computer Science*, vol. 9, no. 3–4, pp. 211–407, 2014.
* <a id="ref-43"></a>[43] M. Abadi, A. Chu, I. Goodfellow, H. B. McMahan, I. Mironov, K. Talwar, and L. Zhang, "Deep learning with differential privacy," in *Proceedings of the 2016 ACM SIGSAC conference on computer and communications security*, 2016, pp. 308–318.
* <a id="ref-44"></a>[44] H. B. McMahan, D. Ramage, K. Talwar, and L. Zhang, "Learning differentially private recurrent language models," *arXiv preprint arXiv:1710.06963*, 2017.
* <a id="ref-45"></a>[45] S. P. Kasiviswanathan, H. K. Lee, K. Nissim, S. Raskhodnikova, and A. Smith, "What can we learn privately?" *SIAM Journal on Computing*, vol. 40, no. 3, pp. 793–826, 2011.
* <a id="ref-46"></a>[46] A. Evfimievski, J. Gehrke, and R. Srikant, "Limiting privacy breaches in privacy preserving data mining," in *Proceedings of the twenty-second ACM SIGMOD-SIGACT-SIGART symposium on Principles of database systems*, 2003, pp. 211–222.
* <a id="ref-47"></a>[47] L. Sun, J. Qian, and X. Chen, "Ldp-fl: Practical private aggregation in federated learning with local differential privacy," *arXiv preprint arXiv:2007.15789*, 2020.
* <a id="ref-48"></a>[48] M. Naseri, J. Hayes, and E. De Cristofaro, "Local and central differential privacy for robustness and privacy in federated learning," *arXiv preprint arXiv:2009.03561*, 2020.
* <a id="ref-49"></a>[49] C. Zhao, S. Zhao, M. Zhao, Z. Chen, C.-Z. Gao, H. Li, and Y.-a. Tan, "Secure multi-party computation: theory, practice and applications," *Information Sciences*, vol. 476, pp. 357–372, 2019.
* <a id="ref-50"></a>[50] Y. Liu, Y. Kang, C. Xing, T. Chen, and Q. Yang, "A secure federated transfer learning framework," *IEEE Intelligent Systems*, vol. 35, no. 4, pp. 70–82, 2020.
* <a id="ref-51"></a>[51] T. Gehlhar, F. Marx, T. Schneider, A. Suresh, T. Wehrle, and H. Yalame, "Safefl: Mpc-friendly framework for private and robust federated learning," in *2023 IEEE Security and Privacy Workshops (SPW)*. IEEE, 2023, pp. 69–76.
* <a id="ref-52"></a>[52] S. Truex, N. Baracaldo, A. Anwar, T. Steinke, H. Ludwig, R. Zhang, and Y. Zhou, "A hybrid approach to privacy-preserving federated learning," in *Proceedings of the 12th ACM workshop on artificial intelligence and security*, 2019, pp. 1–11.
* <a id="ref-53"></a>[53] H. Wang and J. Xu, "Combating client dropout in federated learning via friend model substitution," *arXiv preprint arXiv:2205.13222*, 2022.
* <a id="ref-54"></a>[54] S. Zawad, A. Anwar, Y. Zhou, N. Baracaldo, and F. Yan, "Hdfl: A heterogeneity and client dropout-aware federated learning framework," in *2023 IEEE/ACM 23rd International Symposium on Cluster, Cloud and Internet Computing (CCGrid)*. IEEE, 2023, pp. 311–321.
* <a id="ref-55"></a>[55] A. Madi, O. Stan, A. Mayoue, A. Grivet-Sébert, C. Gouy-Pailler, and R. Sirdey, "A secure federated learning framework using homomorphic encryption and verifiable computing," in *2021 Reconciling Data Analytics, Automation, Privacy, and Security: A Big Data Challenge (RDAAPS)*. IEEE, 2021, pp. 1–8.
* <a id="ref-56"></a>[56] J. Park and H. Lim, "Privacy-preserving federated learning using homomorphic encryption," *Applied Sciences*, vol. 12, no. 2, p. 734, 2022.
* <a id="ref-57"></a>[57] Z. Shi, Z. Yang, A. Hassan, F. Li, and X. Ding, "A privacy preserving federated learning scheme using homomorphic encryption and secret sharing," *Telecommunication Systems*, vol. 82, no. 3, pp. 419–433, 2023.
* <a id="ref-58"></a>[58] Z. Yang, S. Hu, and K. Chen, "Fpga-based hardware accelerator of homomorphic encryption for efficient federated learning," *arXiv preprint arXiv:2007.10560*, 2020.
* <a id="ref-59"></a>[59] F. Tang, G. Ling, C. Cai, J. Shan, X. Liu, P. Tang, and W. Qiu, "Solving small exponential ECDLP in ec-based additively homomorphic encryption and applications," *IEEE Transactions on Information Forensics and Security*, vol. 18, pp. 3517–3530, 2023.
* <a id="ref-60"></a>[60] H. Zhu, R. Wang, Y. Jin, K. Liang, and J. Ning, "Distributed additive encryption and quantization for privacy preserving federated deep learning," *Neurocomputing*, vol. 463, pp. 309–327, 2021.
* <a id="ref-61"></a>[61] Q. Xie, S. Jiang, L. Jiang, Y. Huang, Z. Zhao, S. Khan, W. Dai, Z. Liu, and K. Wu, "Efficiency optimization techniques in privacy-preserving federated learning with homomorphic encryption: A brief survey," *IEEE Internet of Things Journal*, vol. 11, no. 14, pp. 24 569–24 580, 2024.
* <a id="ref-62"></a>[62] J. Qian, K. Wei, Y. Wu, J. Zhang, J. Chen, and H. Bao, "Gi-smn: Gradient inversion attack against federated learning without prior knowledge," in *International Conference on Intelligent Computing*. Springer, 2024, pp. 439–448.
* <a id="ref-63"></a>[63] Y. Zhao, J. Chen, J. Zhang, Z. Yang, H. Tu, H. Han, K. Zhu, and B. Chen, "User-level membership inference for federated learning in wireless network environment," *Wireless Communications and Mobile Computing*, vol. 2021, no. 1, p. 5534270, 2021.
* <a id="ref-64"></a>[64] I. Driouich, C. Xu, G. Neglia, F. Giroire, and E. Thomas, "Local model reconstruction attacks in federated learning and their uses," *arXiv preprint arXiv:2210.16205*, 2022.
* <a id="ref-65"></a>[65] M. J. Mia and M. H. Amini, "A secure object detection technique for intelligent transportation systems," *IEEE Open Journal of Intelligent Transportation Systems*, 2024.
* <a id="ref-66"></a>[66] Y. Qiu, H. Yu, H. Fang, W. Yu, B. Chen, X. Wang, S.-T. Xia, and K. Xu, "Mibench: A comprehensive benchmark for model inversion attack and defense," *arXiv preprint arXiv:2410.05159*, 2024.
* <a id="ref-67"></a>[67] X. Zhang and X. Luo, "Exploiting defenses against gan-based feature inference attacks in federated learning," *arXiv preprint arXiv:2004.12571*, 2020.
* <a id="ref-68"></a>[68] K. Chen, W. Wang, Z. Wang, Y. Huang, Y. Xiao, W. Zhang, Z. Li, Z. Guo, Z. Luo, L. Yin *et al.*, "Private data leakage in federated contrastive learning networks," *IEEE Open Journal of the Communications Society*, 2024.
* <a id="ref-69"></a>[69] A. Benaissa, B. Retiat, B. Cebere, and A. E. Belfedhal, "Tenseal: A library for encrypted tensor operations using homomorphic encryption," *arXiv preprint arXiv:2104.03152*, 2021.
* <a id="ref-70"></a>[70] A. Krizhevsky, G. Hinton *et al.*, "Learning multiple layers of features from tiny images," 2009.
* <a id="ref-71"></a>[71] Y. LeCun, "The mnist database of handwritten digits," *http://yann. lecun. com/exdb/mnist/*, 1998.
* <a id="ref-72"></a>[72] H. A. Salehi, M. J. Mia, S. S. Pradhan, M. H. Amini, and F. Shirani, "Corbin-fl: A differentially private federated learning mechanism using common randomness," *arXiv preprint arXiv:2409.13133*, 2024.

## TL;DR
Research on quancrypt-fl: quantized homomorphic encryption with pruning for secure federated learning providing insights for knowledge graph development and data integration.

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