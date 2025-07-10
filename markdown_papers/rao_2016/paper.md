---
cite_key: rao_2016
title: A Selective Homomorphic Encryption Approach for Faster Privacy-Preserving Federated Learning
authors: Abdulkadir Korkmaz · Praveen Rao
year: 2016
date_processed: '2025-07-02'
phase2_processed: true
original_folder: arxiv_2501.12911_A_Selective_Homomorphic_Encryption_Approach_for_Faster_Privacy-Preserving_Federated_Learning
images_total: 18
images_kept: 18
images_removed: 0
tags:
- Blockchain
- Federated Learning
- Healthcare
- Machine Learning
- Privacy
keywords:
- differential privacy
- federated learning
- fedml-he
- fhe
- homomorphic encryption
- machine learning
- privacy-preserving
- trade-off
---

# A Selective Homomorphic Encryption Approach for Faster Privacy-Preserving Federated Learning

Abdulkadir Korkmaz · Praveen Rao

Abstract Federated learning (FL) has come forward as a critical approach for privacy-preserving machine learning in healthcare, allowing collaborative model training across decentralized medical datasets without exchanging clients' data. However, current security implementations for these systems face a fundamental trade-off: rigorous cryptographic protections like fully homomorphic encryption (FHE) impose prohibitive computational overhead, while lightweight alternatives risk vulnerable data leakage through model updates. To address this issue, we present FAS (Fast and Secure Federated Learning), a novel approach that strategically combines selective homomorphic encryption, differential privacy, and bitwise scrambling to achieve robust security without compromising practical usability. Our approach eliminates the need for model pretraining phases while dynamically protecting highrisk model parameters through layered encryption and obfuscation. We implemented FAS using the Flower framework and evaluated it on a cluster of eleven physical machines. Our approach was up to 90% faster than applying FHE on the model weights. In addition, we eliminated the computational overhead that is required by competitors such as FedML-HE and MaskCrypt. Our approach was up to 1.5× faster than the competitors while achieving comparable security results.

Experimental evaluations on medical imaging datasets confirm that FAS maintains similar security results to conventional FHE against gradient inver-

A. Korkmaz

## P. Rao

sion attacks while preserving diagnostic model accuracy. These results position FAS as a practical solution for latency-sensitive healthcare applications where both privacy preservation and computational efficiency are requirements.

Keywords Federated learning · medical image datasets · secure · privacy-preserving · machine learning

### 1 Introduction

Federated learning (FL), first introduced by Google in 2016, enables machine learning models to be trained across decentralized datasets stored on distributed devices such as mobile phones [1]. This method has gained widespread interest across academia and industry because of its effectiveness in safeguarding data privacy. By keeping training data localized and only sharing model updates, FL avoids direct data exposure, making it particularly valuable in regulated sectors like healthcare. For instance, hospitals can collaboratively train diagnostic models without transferring sensitive patient records, ensuring compliance with privacy regulations.

Nonetheless, the decentralized structure of FL brings about distinct security challenges. While data remains on local devices, the transmission of model parameters over networks creates vulnerabilities, including risks of unauthorized access or data leakage during exchange. Existing research often assumes that data localization inherently guarantees privacy, overlooking these communication-phase threats. Current security strategies in FL, such as encrypting communication channels or perturbing shared gradients, are frequently implemented in isolation, without systematic analysis of their combined impact on computational efficiency, model accuracy, or multi-layered privacy preservation.

Dept. of Electrical Engineering & Computer Science, The University of Missouri, Columbia, USA E-mail: ak69t@umsystem.edu

Dept. of Electrical Engineering & Computer Science, The University of Missouri, Columbia, USA E-mail: praveen.rao@missouri.edu

Recent advances, such as FedML-HE [18] and MASKCRYPT [19], attempt to address these challenges through selective encryption. FedML-HE employs gradient sensitivity analysis during pre-training to identify critical weights for HE, but its reliance on clientspecific masks introduces aggregation inconsistencies and computational overhead. MASKCRYPT optimizes gradient-guided masks to reduce communication costs, yet its security requires multiple rounds to stabilize, leaving early training phases vulnerable. Both methods incur significant computational penalties—FedML-HE from pre-training and MASKCRYPT from per-round mask recalibration—while struggling to balance realtime efficiency with robust privacy guarantees. These constraints point to the necessity of a cohesive solution that removes the need for initialization phases, reduces computational effort per round, and maintains stable security throughout all FL rounds.

Motivated by the aforementioned reasons, we propose FAS (Fast and Secure Homomorphic Encryption), a novel method designed to address these gaps by unifying cryptology-based security mechanisms tailored for federated architectures. Unlike FedML-HE and MASKCRYPT, FAS eliminates pre-training phases and per-round mask recalibration, instead combining selective homomorphic encryption with noise-andscrambling mechanisms to secure a fixed percentage of model weights. This ensures consistent privacy guarantees from the first training round while minimizing computational overhead. We present a comparative study of FAS against conventional HE, differential privacy, and state-of-the-art baselines (FedML-HE and MASKCRYPT). Through simulations across cloud-based federated environments and diverse medical imaging datasets (e.g., Kidney, Lung, COVID), we rigorously measure how each method balances privacy protection, computational efficiency, and model utility.

To validate FAS's efficacy, we conducted extensive experiments across medical imaging tasks and model architectures. Our evaluation shows that FAS offers high efficiency comparable to leading methods, all while preserving strong privacy protections. On datasets like Kidney and COVID, FAS reduced encryption overhead by up to 90% compared to FHE, with training times as low as 52 minutes for MobileNetV2 (vs. 610 minutes for full encryption). Crucially, FAS eliminated the pre-training and mask recalibration costs inherent to FedML-HE and MASKCRYPT, achieving 1.5×× faster execution than these baselines (e.g., 69 vs. 99 minutes for EffNetB0 on Kidney data). Security evaluations using MSSIM and VIFP confirmed that even at 10% encryption, FAS effectively thwarts model inversion attacks, with MSSIM

scores of 58%—outperforming FedML-HE (52%) and MASKCRYPT (55%) in early-round privacy. FAS's VIFP scores stabilized within 5 rounds, contrasting with MASKCRYPT's delayed convergence. This combination of speed and robustness positions FAS as a practical solution for latency-sensitive federated deployments, where traditional methods trade excessive computation for marginal security gains.

## Our key contributions are as follows:

- Implementation of Security Techniques: We implement three security mechanisms—HE [16], differential privacy [15], and the proposed FAS technique—within a FL framework, demonstrating their operational feasibility.
- Development of FAS: We design a novel Fast and Secure Homomorphic Encryption method that integrates selective encryption with noise injection and bitwise scrambling to enhance security while maintaining computational efficiency.
- Performance Evaluation: We conduct a comprehensive comparison of encryption techniques using standardized metrics (MSSIM, VIFP) to assess their computational overhead, scalability, and resistance against model inversion attacks.
- Practical Insights: We characterize the trade-offs between privacy guarantees and system performance, offering implementable guidelines for deploying secure FL in real-world scenarios.

Experimental results demonstrate that FAS achieves superior balance between security and efficiency compared to conventional methods, particularly in latency-sensitive applications like healthcare systems where privacy and responsiveness are critical.

### 2 Background and Related Work

Privacy-preserving techniques in FL have gained significant attention due to the critical need to protect sensitive data across distributed devices. FL, initially introduced by McMahan et al. [23], enables decentralized model training by sharing parameter updates instead of raw data. However, this approach introduces inherent risks of data leakage through exposed model gradients, necessitating robust cryptographic safeguards to prevent adversarial reconstruction of private datasets.

## 1 Efficiency Enhancements in Homomorphic Encryption

HE has emerged as a foundational technology for secure computation on encrypted data. Gentry's pioneering FHE scheme [16] first demonstrated the feasibility of arbitrary computations on ciphertexts, though its substantial computational overhead limited practical adoption. Subsequent research has focused on optimizing efficiency:

Fan and Vercauteren's BGV Scheme [25] introduced optimizations to the bootstrapping process, enabling faster processing of encrypted data by supporting basic arithmetic functions such as summation and product computations. This advancement significantly improved the practicality of HE for complex computations in FL environments, as further validated by Smart and Vercauteren [33].

Chillotti et al.'s TFHE Scheme [26] achieved faster bootstrapping for secure Boolean operations, making FHE viable for real-time applications requiring rapid iterative computations. Ducas and Micciancio's FHEW Scheme [27] further accelerated homomorphic operations through bootstrapping refinements, broadening HE's applicability to large-scale distributed systems.

Cheon et al.'s CKKS Scheme [29] addressed machine learning use cases by supporting approximate arithmetic on encrypted data, prioritizing computational efficiency over exact precision. Brakerski, Gentry, and Vaikuntanathan's BGV+ Scheme [28] introduced noise management optimizations to preserve model accuracy under encryption.

Xu et al. [41] proposed HybridAlpha, a FL system combining differential privacy with secure aggregation to balance privacy and performance. While HybridAlpha reduces computational overhead compared to pure HE approaches, its reliance on generic privacy mechanisms leaves room for optimizations tailored to federated workflows.

2.2 Differential Privacy (DP) in Federated Learning

Differential Privacy (DP) reduces the risk of sensitive data exposure by perturbing model updates with controlled noise throughout the training phase. First formalized by Dwork et al. [30], DP was later adapted to deep learning by Abadi et al. [31], who developed the DP-SGD algorithm to protect training data. Mironov et al. [35] refined these concepts using R´enyi differential privacy, providing tighter privacy budget analysis for iterative machine learning processes. Despite these advancements, DP-based methods inherently degrade model utility due to noise injection, particularly in precision-sensitive applications like medical imaging.

## 3 Selective Encryption in Federated Learning

Selective encryption strategies aim to reduce computational overhead by encrypting only sensitive subsets of model parameters. Wu et al. [32] demonstrated that selectively encrypting critical gradients preserves privacy while maintaining computational feasibility. Li et al. [37] and Song et al. [38] expanded this concept with adaptive parameter selection criteria, though their methods require careful tuning to avoid residual vulnerabilities.

Zhang et al. [45] introduced BatchCrypt, a HE framework that batches model updates to reduce communication and computation costs. While BatchCrypt improves efficiency over traditional HE methods, its encryption scope remains inflexible for dynamic FL scenarios. This paper extends prior work by integrating selective encryption with differential noise injection and bitwise scrambling, achieving enhanced privacy with reduced computational overhead.

## 4 Bitwise Scrambling for Federated Learning Security

Bitwise scrambling enhances security by nonlinearly rearranging bits in partially encrypted data using cryptographic keys. Yang et al. [24] applied scrambling to secure data transmissions against reconstruction attacks, demonstrating its effectiveness as a lightweight obfuscation layer. Halevi et al. [39] combined scrambling with HE to resist chosen-ciphertext attacks while maintaining computational efficiency.

The combination of selective encryption, differential privacy, and bitwise scrambling provides a multi-layered defense mechanism for FL systems. This integrated approach balances security robustness with practical efficiency, addressing the resource constraints inherent in distributed edge computing environments.

## 3 Motivation and Threat Model

### 1 Motivation

Applying FL to sensitive domains like healthcare and finance underscores a key issue: decentralized training by itself is insufficient to stop adversaries from uncovering sensitive patterns through exposed model updates. While FL avoids raw data centralization, empirical studies confirm that transmitted gradients retain sufficient information for model inversion attacks to reconstruct patient scans, financial transactions, or other identifiable records—even when training adheres to protocol.

Existing privacy mechanisms force practitioners into suboptimal trade-offs. FHE provides cryptographically rigorous confidentiality but imposes prohibitive computational latencies, rendering it impractical for realtime medical diagnostics or high-frequency trading systems. Differential privacy (DP), while computationally lightweight, irreversibly corrupts model updates with statistical noise, degrading diagnostic accuracy in oncology imaging or fraud detection below clinically/operationally viable thresholds.

Our FAS framework addresses this dichotomy through context-aware privacy stratification. By selectively encrypting only high-risk parameters (e.g., gradients correlating with identifiable features), applying tunable DP noise to less sensitive components, and augmenting both with bitwise scrambling, FAS maintains diagnostic-grade model utility while eliminating cryptographic overheads associated with full-model FHE. Crucially, this multi-tiered protection operates without requiring precomputed sensitivity masks or auxiliary pretraining phases, ensuring seamless integration into latency-constrained FL pipelines for MRI analysis, genomic prediction, and other precision-sensitive applications.

### 2 Threat Model

FL systems are susceptible to privacy threats due to decentralized training and the exchange of model updates. A semi-honest attacker may adhere to the protocol while still trying to extract confidential information from observed or compromised data.

Model updates shared between clients and the central server may be intercepted by attackers. Common attack vectors include gradient inversion to reconstruct training data, membership inference to verify specific data participation, and statistical analysis to infer private attributes. While SSL encryption secures transmissions, it does not prevent adversaries from analyzing transmitted updates.

To mitigate these risks, our approach integrates selective encryption, differential noise addition, and bitwise scrambling. Critical model parameters are encrypted, while unencrypted data is obfuscated with noise and scrambling to prevent reconstruction. Secure aggregation further ensures data protection throughout training, providing strong defenses against privacy attacks without incurring excessive computational overhead. This layered strategy effectively balances security and efficiency, making it well-suited for sensitive applications like healthcare.

### 4 Proposed Model

This research presents FAS (Fast and Secure Federated Learning), a novel privacy-preserving scheme designed to reduce the computational cost of encryption while maintaining strong protection against privacy threats. The model integrates three lightweight techniques— selective encryption, differential noise addition, and bitwise scrambling along with HE—into the FL process. This multi-pronged approach enhances security without the heavy overhead typically associated with FHE or the accuracy degradation often introduced by differential privacy when used in isolation.

### 1 Selective Encryption

Instead of encrypting all model parameters, FAS applies HE only to a fixed percentage of the weights, selected uniformly. This subset is treated as the most sensitive part of the model. The encryption is performed directly on these weights using a homomorphic scheme, allowing the server to carry out aggregation without requiring decryption. This design choice retains the advantages of HE while reducing the time and resource demands substantially, achieving up to 90% reduction in overhead compared to full encryption.

### 2 Differential Noise

To reinforce privacy for the remaining (unencrypted) parameters, the model introduces controlled random noise. This noise follows a Laplace distribution and is calibrated using differential privacy principles. While FAS does not rely solely on differential privacy for security, this mechanism makes individual contributions harder to isolate, especially in low-sensitivity weights. By blending noise into less critical parameters, the model increases resistance to membership inference attacks with minimal impact on performance.

### 3 Bitwise Scrambling

FAS further obfuscates unencrypted data through bitwise scrambling. A lightweight cryptographic key is used to permute the bits of the non-encrypted parameters. This process disrupts patterns and statistical properties that could be exploited by adversaries. When combined with noise, scrambling ensures that unencrypted parts of the model are still resistant to reconstruction attacks—even in the presence of partial knowledge or auxiliary data.

### 4 Federated Learning Integration

FAS is designed to integrate directly into standard FL workflows. At each round, clients:

- 1. Train their local models on private data.
- 2. Encrypt a portion of the model weights.
- 3. Apply scrambling and noise to the rest.
- 4. Transmit the transformed updates to the server.

The server merges the incoming gradients using techniques like weighted averaging. Following this, a scrambling key is applied to the aggregated model before it is sent back to the clients, where it is decrypted and used for continued training.

### 5 Security and Efficiency Trade-Off

The proposed system achieves a balance between security and speed:

- Security: FAS protects sensitive parameters through encryption while mitigating risks to the remaining ones through obfuscation. This layered defense shows comparable robustness to fully encrypted models in resisting attacks like model inversion and membership inference.
- Efficiency: By reducing the encryption scope and avoiding pre-processing phases like sensitivity masking, FAS cuts down overhead significantly. It is particularly well-suited for settings with limited computational power.

By integrating selective encryption, noise injection, and scrambling, this approach offers a practical and deployable solution for secure FL in privacy-sensitive areas, including medical and financial domains.

### 6 Privacy-Preserving Techniques

### 6.1 Homomorphic Encryption

Homomorphic encryption (HE) is a cryptographic scheme that permits data processing to occur while the data remains encrypted, eliminating the need for decryption during computation.

In the context of FL, HE enables secure aggregation of model updates from distributed clients. The mathematical foundation of HE ensures that:

$$
Dec(Eval(Enc(x), Enc(y))) = f(x, y),
$$

where Enc and Dec refer to the encryption and decryption functions, respectively, and Eval denotes a computation performed on ciphertexts. This capability is

![](_page_4_Figure_19.jpeg)
<!-- Image Description: The flowchart depicts a federated learning system. Two clients ("Client 1" and "Client 2") independently train on weight vectors, then encrypt and obfuscate the results (bitwise scramble, random encrypt, differential noise). These encrypted updates are sent to a central server which aggregates them. The aggregated model is then distributed as a model update back to the clients. The diagram illustrates the process of secure model aggregation in a federated learning setting. -->

Figure 1 General depiction of the FL model showing the processes of encryption, scrambling, and aggregation.

essential for privacy-preserving scenarios, as it ensures that plaintext data remains inaccessible to potential adversaries. [16].

### 6.2 Differential Privacy

Differential Privacy (DP) is a privacy framework that adds carefully calibrated noise to statistical outputs, ensuring that individual data points have minimal impact on the overall resul.

A mechanism M is said to ensure ϵ-differential privacy if, for all subsets of outputs O and for any pair of datasets D<sup>1</sup> and D<sup>2</sup> that differ by only one record, the following holds:

$$
\frac{\Pr[M(D_1) \in O]}{\Pr[M(D_2) \in O]} \le e^{\epsilon},
$$

where ϵ represents the privacy parameter. [30].

In FL, DP adds noise to model updates or gradients prior to aggregation, shielding individual data contributions while retaining overall model performance. This makes DP particularly useful for safeguarding privacy in high-stakes sectors like medical and financial applications.

### 7 Process Flow of the Proposed Model

The proposed model follows a three-stage pipeline: client-side processing, server-side processing, and client post-processing. Each phase includes well-defined steps illustrated with pseudocode and supported by visual diagrams.

Figure 1 provides a general depiction of our FL model, demonstrating the encryption, scrambling, and noise addition steps across client nodes, and the subsequent aggregation performed by the server.

![](_page_5_Figure_0.jpeg)
<!-- Image Description: This flowchart illustrates a data processing pipeline for secure model training. "Train" data undergoes random weight vector splitting, encryption, hexadecimal formatting, noise addition, bitwise scrambling with a key, and finally transmission to a server. The diagram details the stages of data obfuscation before sending it to the server, likely to protect sensitive training data. -->

Figure 2 Client-side process in FL system: encryption, scrambling, and noise addition.

![](_page_5_Figure_2.jpeg)
<!-- Image Description: This flowchart illustrates a secure aggregation protocol. Client vectors are split, with one part encrypted and the other not. The server receives these parts, aggregates the encrypted portions separately from the non-encrypted ones, and then combines them before sending the result back to the clients, ensuring privacy. The diagram details the data flow and encryption/aggregation steps. -->

Figure 3 Server-side process in FL system: aggregation and rescrambling.

Figure 1 presents a general overview of the FL system, encompassing client-side encryption, scrambling, noise addition, and server-side aggregation. Figures 2 and 3 illustrate the detailed client and server sides workflows, respectively.

The process begins at the client side, where local data is utilized to train a model, producing a weight vector. This weight vector is split, encrypted, and further obfuscated through bitwise scrambling and the addition of noise.

Once encrypted, the weight vectors are formatted to hexadecimal and transmitted to the server. The server subsequently collects encrypted model data from all clients and applies federated averaging (FedAvg) to combine the parameters. Importantly, the aggregation is done on both encrypted and non-encrypted vectors, ensuring privacy is maintained while also allowing for more efficient computation.

After aggregation, the server mixes the results with a scrambling key before sending the updated parameters back to the clients, where they are decrypted and applied to the local models for further training.

This privacy-aware and secure approach facilitates effective model training on decentralized data, while safeguarding sensitive information from unauthorized access.

## 7.1 Client-Side Processing

In the client-side processing stage, model weights (w) are prepared for secure transmission to the server by encrypting selected weights, obfuscating the remaining weights, and combining them into a single data structure. Initially, the weights are split into two subsets based on a predefined encryption percentage (enc pct) (Lines 6–8). The selected portion of the weights is encrypted using a HE function (enc func), and these encrypted weights are stored in enc w (Lines 9–11). For the remaining weights, they are first formatted to resemble encrypted data (fmt weight), noise is added using noise func, and the noisy weights are scrambled with a cryptographic key (scr key) via a scrambling function (scr func) (Lines 12–16). These scrambled weights are stored in scr w. Finally, the encrypted and scrambled weights are combined into a single structure (enc scr w) (Line 17) and transmitted to the server (Line 18).

Algorithm 1 Client-Side Enc, Scrambling, and Noise Addition

- Require: 1: w: Model weights
- 2: enc pct: Percentage of weights to encrypt
- 3: enc func: Encryption function
- 4: scr key: Scrambling key
- 5: scr func: Scrambling function
- 6: noise func: Noise addition function
- Ensure:
- 7: enc scr w: Processed (encrypted and scrambled) weights 8: procedure Client Enc-Scr-Noise
- 9: Split w into encrypted and non-encrypted parts
- 10: n ← length of w
- 11: num enc ← (enc pct/100) ∗ n
- 12: enc w ← []
- 13: scr w ← []
- 14: for i = 0 to num enc − 1 do
- 15: enc weight ← enc func(w[i])
- 16: Append enc weight to enc w
- 17: end for
- 18: for i = num enc to n − 1 do
- 19: fmt weight ← format as encrypted(w[i])
- 20: noisy weight ← noise func(fmt weight)
- 21: scr weight ← scr func(noisy weight,scr key)
- 22: Append scr weight to scr w
- 23: end for
- 24: Combine enc w and scr w into enc scr w
- 25: Send enc scr w to the server

26: end procedure

## 7.2 Server-Side Processing

On the server side, the received combined weights (enc scr w) are processed to aggregate updates securely without decryption. The scrambled weights are first unscrambled using the same cryptographic key (scr key) applied during client-side processing (Lines 5–7). Once unscrambled, these weights are aggregated using a processing function (srv proc func) (Lines 8– 9). Homomorphic operations are applied directly on the encrypted weights without decryption (Line 9). After processing, the unscrambled weights are reformatted and scrambled again using scr func and scr key to preserve security (Lines 10–13). These processed and re-scrambled weights are then combined with the processed encrypted weights and sent back to the client (Line 14).

| Algorithm 2 Server-Side Processing without Decryp | | | |
|---------------------------------------------------|--|--|--|
| tion | | | |
| Require: | | | |

| 1: enc scr w: Received weights from client | | |
|--------------------------------------------|--|--|

- 2: scr key: Scrambling key for re-scrambling
- 3: srv proc func: Server processing function

## Ensure:

4: sec w: Processed weights sent back to client

- 5: procedure Server Proc w/o Decrypt
- 6: Receive enc scr w from the client
- 7: proc w ← []
- 8: unscr w ← []
- 9: for w in scr w do
- 10: unscr weight ← unscramble func(w, scr key)
- 11: Append unscr weight to unscr w
- 12: end for
- 13: Process unscr w using srv proc func
- 14: Process enc w using homomorphic operations (no decryption needed)
- 15: Format unscr w back to scrambled format:
- 16: for w in unscr w do
- 17: re scr w ← scr func(w, scr key)
- 18: Append re scr w to proc w
- 19: end for
- 20: Combine proc enc w with re scr w
- 21: Send sec w back to the client
- 22: end procedure

### 7.3 Client Post-Processing

In the final stage, the client receives the processed weights (sec w) from the server (Line 2) and restores them for updating the local model. The encrypted subset of weights is decrypted using the appropriate decryption function (Lines 3–4), while the scrambled weights are unscrambled with the cryptographic key (scr key) to restore their original form (Lines 5–7). These two subsets of weights are then combined to reconstruct the full model weights (Line 8), which are subsequently used to refine the model instance residing on the client for the next round of federated learning. (Line 9).

4.8 Advantages of the Proposed Model

- Enhanced Security: The combination of encryption, noise, and scrambling protects both encrypted and unencrypted data.
- Efficiency: Reduces computational overhead by selectively encrypting only a portion of the weights.

| | Algorithm | 3 | Client | Post-Processing | with | Noise | | |
|-------------------------------------------------|----------------------------------------|---|--------|---------------------------------------------------|------|-------|--|--|
| | Restoration | | | | | | | |
| | Require: | | | | | | | |
| | 1: sec w: Weights received from server | | | | | | | |
| | | | | 2: scr key: Scrambling key for restoration | | | | |
| Ensure: | | | | | | | | |
| | | | | 3: f inal w: Updated model weights for next round | | | | |
| 4: procedure Client Post-Proc with Noise Rest | | | | | | | | |
| 5:<br>Receive sec w from the server | | | | | | | | |
| 6:<br>proc enc w ← sec w[0 : num enc] | | | | | | | | |
| 7:<br>proc scr w ← sec w[num enc :] | | | | | | | | |
| 8:<br>for w in proc scr w do | | | | | | | | |
| restored w ← reverse scr func(w, scr key)<br>9: | | | | | | | | |
| 10: | | | | Append restored w to rest w | | | | |
| 11: | end for | | | | | | | |
| 12: | | | | Combine proc enc w and rest w to form f inal w | | | | |
| 13: | | | | Proceed to next round of FL with f inal w | | | | |

– Scalability: Optimized for large-scale FL systems with multiple clients.

### 9 Privacy Analysis

14: end procedure

This section presents a provide a formal analysis demonstrating that our FL mechanism—integrating selective homomorphic encryption, differential privacy, and bitwise scrambling—upholds a clear and measurable differential privacy guarantee.

### 9.1 Setup and Definitions

We consider a FL setting with n clients, each holding private data. The global model is described by parameters indexed by [N]. Let S ⊆ [N] be the subset of parameters to be protected by selective homomorphic encryption , and let [N]\S be the remaining parameters to which we add differential privacy (DP) noise.

Differential Privacy. A mechanism M satisfies ϵdifferential privacy if, for any neighboring datasets D and D′ (differing in one element), and for every measurable set of outputs O, it holds that:

$$
\frac{\Pr[M(D) \in O]}{\Pr[M(D') \in O]} \le e^{\epsilon}.
$$

[30]

Selective Homomorphic Encryption. Parameters in S are encrypted using a semantically secure HE scheme. Semantic security ensures no polynomial-time adversary can distinguish ciphertexts of different messages, implying no additional privacy cost in a DP sense (0- DP).[16]

each i ∈ [N] \ S, we add noise calibrated to ϵi-DP. By the composition property of DP, releasing all these parameters together is P i∈[N]\S ϵi -DP.[30]

Bitwise Scrambling. We define a scrambling function T<sup>k</sup> : X → X , where X is the space of possible model outputs. T<sup>k</sup> is deterministic, keyed by k, and independent of D except through M(D). This scrambling is a form of post-processing.[43]

## 9.2 Privacy Guarantee

Theorem 1 Consider a mechanism M that on input dataset D:

- 1. Encrypts W<sup>i</sup> for i ∈ S using a semantically secure HE scheme [16, 44].
- 2. Adds noise to each W<sup>j</sup> for j ∈ [N] \ S to achieve ϵ<sup>j</sup> -DP. Releasing all noisy parameters together is P j∈[N]\S ϵj -DP [42].
- 3. Applies a scrambling function T<sup>k</sup> to the entire output, resulting in M′ (D) = Tk(M(D)) [43].

Then,
$$
\mathcal{M}'(D)
$$
is also $\left(\sum_{j\in[N]\setminus S}\epsilon_j\right)$ -DP.

Proof Step 1 (DP on [N] \ S): For [N] \ S, each parameter W<sup>j</sup> +noise<sup>j</sup> is ϵ<sup>j</sup> -DP. By composition, releasing all these parameters is P j∈[N]\S ϵ<sup>j</sup> -DP [42]. Formally, for any adjacent D, D′ and event O:

$$
\frac{\Pr[\mathcal{M}_{[N]\setminus S}(D)\in O]}{\Pr[\mathcal{M}_{[N]\setminus S}(D')\in O]} \le e^{\sum_{j\in [N]\setminus S}\epsilon_j[42]}.
$$

.

Step 2 (Selective Encryption on S): Parameters in S are encrypted with a semantically secure HE scheme. Without the secret key, no information about the plaintext is revealed, contributing 0-DP cost [16, 44].

Step 3 (Scrambling as Post-Processing): The scrambling function T<sup>k</sup> operates as a deterministic transformation that does not depend on the underlying data. A core principle of differential privacy is that its guarantees are preserved under any data-independent transformation. Specifically, if a mechanism M satisfies ϵ-DP, then so does f(M) for any deterministic function f [43, 42].

Combining these results:

$$
\frac{\Pr[\mathcal{M}'(D) \in O]}{\Pr[\mathcal{M}'(D') \in O]} = \frac{\Pr[\mathcal{T}_k(\mathcal{M}(D)) \in O]}{\Pr[\mathcal{T}_k(\mathcal{M}(D')) \in O]} \le e^{\sum_{j \in [N] \setminus S} \epsilon_j}.
$$

Thus, M′ (D) maintains the same DP guarantee as M(D).

![](_page_7_Figure_17.jpeg)
<!-- Image Description: The image displays sample chest X-ray images categorized into three groups: (a) Benign, (b) COVID-19, and (c) Pneumonia. Each group shows four example X-rays, illustrating the visual differences in lung patterns associated with each condition. The image serves as a visual representation of the dataset used in the paper, showcasing the variations in radiological findings used for model training and evaluation. -->

Figure 4 Examples from the Chest X-ray (Covid, Pneumonia) dataset [20]

### 5 Evaluation

This section evaluates our FL setup using various security techniques, including HE, differential privacy, and our proposed FAS. We assess their impact on test accuracy, communication cost, computational overhead, and privacy preservation.

Each dataset was divided into 10 equal parts and assigned to separate machines operating as Flower [11] clients. Each client trained its local model over 10 rounds, performing 20 epochs per round. A validation set, comprising 10% of the training data, was used to maintain consistency, while final accuracy was measured on an independent test set. All models were trained using CPU resources to simulate realistic constraints.

### 1 Datasets Used in Experiments

We selected publicly available datasets covering diverse imaging contexts with high usability ratings. Our criteria included broad disease coverage, diverse imaging techniques, and sufficient training and validation data.

### 1.1 CIFAR-10 Dataset [46]

A benchmark for image classification, CIFAR-10 consists of 60,000 32x32 images across 10 classes. It includes 50,000 training and 10,000 test images, commonly used for model performance evaluation.

## 1.2 Chest X-ray (COVID-19, Pneumonia) Dataset [7]

This dataset contains 6,339 grayscale X-ray images across three classes: benign, COVID-19, and pneumonia (2,313 images per class). These images aid in lung condition assessment.

## 1.3 CT Kidney Dataset [9]

Comprising 12,446 CT scans categorized as benign (5,077), cyst (3,709), stone (1,377), and tumor (2,283), this dataset aids in kidney disease diagnosis.

![](_page_8_Figure_1.jpeg)
<!-- Image Description: This image displays four sets of axial computed tomography (CT) scans of kidneys, each set representing a different kidney pathology: benign, cyst, stone, and tumor. Each set shows three to four different slices of the same kidney at varying depths. The purpose is to visually illustrate the distinct CT scan appearances of these kidney conditions, likely for diagnostic comparison or algorithm training in the context of the paper. -->

Figure 5 Examples from the CT Kidney dataset [20]

![](_page_8_Figure_3.jpeg)
<!-- Image Description: The image presents two sets of retinal fundus photographs. (a) shows four examples of benign retinas, while (b) displays four examples of retinas with diabetic retinopathy. The image serves as a visual comparison to illustrate the differences in retinal appearance between healthy and diseased states, likely within a section on image data used for a diagnostic model in the paper. -->

Figure 6 Examples from the Diabetic Retinopathy Detection dataset [20]

![](_page_8_Figure_5.jpeg)
<!-- Image Description: The image displays microscopic tissue samples categorized into three groups: (a) Benign, (b) Adenocarcinoma (ACC), and (c) Squamous Cell Carcinoma (SCC). Each group presents four 2x2 arrays of histological images, visually illustrating the distinct microscopic appearances of these tissue types. The purpose is to provide a visual representation of the data used in the paper for classification or analysis of cancerous and benign tissues. -->

Figure 7 Examples from the Lung Cancer Histopathological Images dataset. [20]

### 1.4 Diabetic Retinopathy Dataset [6]

This dataset comprises 88,645 fundus images, categorized as benign (65,342) or diabetic retinopathy (23,303). Fundus imaging assists in detecting optic nerve abnormalities.

### 1.5 Lung Cancer Histopathological Images [8]

This dataset contains 15,000 histopathological images, equally distributed across benign, squamous cell carcinoma (SCC), and adenocarcinoma (ACC) classes.

## 6 Experimental Setup

This section outlines the experimental framework employed to assess different cryptographic methods within a FL environment applied to medical imaging datasets.

## 1 CloudLab Environment

Experiments were conducted on CloudLab [10], a cloud computing testbed for systems research. The experimental setup consisted of 11 standalone physical machines in a shared-nothing cluster, interconnected through 10 Gbps Ethernet. Each machine featured dual Intel E5-2683 v3 CPUs (14 cores at 2.00 GHz), 256 GB of RAM, and a pair of 1 TB hard drives, offering ample computational capacity for FE workloads.

### 2 Federated Learning Framework: Flower

Flower [11], an open-source FL framework, was used for model training and evaluation, supporting Tensor-Flow [12], PyTorch [13], and MXNet [14]. One Cloud-Lab machine served as the Flower server, while the remaining 10 functioned as Flower clients.

### 3 Federated Learning Setup

Each dataset was divided into 10 equal partitions, distributed across the Flower clients. The centralized FL setup comprised 10 clients and a server. Each model was trained over 10 rounds, with 20 epochs per round. A validation set (10% of training data) monitored performance, and final accuracy was evaluated on a test set. All training used CPUs to simulate resourceconstrained environments.

### 4 Rationale for Centralized Federated Learning

Decentralized FL was not used due to a lack of mutual trust among clients. A centralized setup ensures data privacy, as clients communicate only with the server, avoiding direct data exchange and aligning with confidentiality requirements.

### 5 Deep Learning Models

We evaluated four deep learning models:

ResNet-50 mitigates the vanishing gradient problem with skip connections, facilitating deep network training.

### 5.2 DenseNet121[3]

DenseNet121 enhances feature reuse by connecting each layer to all previous layers, improving efficiency in resource-constrained settings.

### 5.3 EfficientNetB0[4]

EfficientNetB0 optimally scales network width, depth, and resolution, balancing accuracy and efficiency.

### 5.4 MobileNet V2[5]

MobileNet V2 leverages efficient convolutional operations to minimize computational overhead while still delivering strong predictive performance, making it wellsuited for deployment on mobile and embedded devices.

### 6 Encryption Configurations

We compared three encryption configurations:

- Non-Enc: No encryption applied.
- Full-Enc: All model weights encrypted using HE.
- Partly-Enc:FAS is applied to a subset of data, with scrambling for security.

Full Overhead represents additional training time due to full encryption, while Partly Overhead captures the impact of FAS.

Table 1 presents training times (minutes) across datasets. Fully encrypted models require significantly more training time, with ResNet-50 showing the highest overhead. In contrast, FAS reduce overhead substantially while maintaining security.

Figure 8 shows communication costs across encryption levels, revealing higher costs for fully encrypted models, whereas FAS optimizes performance.

Figure 9 indicates that accuracy remains stable across encryption percentages, confirming the effectiveness of FAS in preserving model performance.

Figure 10 highlights significant reductions in encryption overhead when using FAS, making FAS a viable option for resource-limited FL scenarios.

Table 1 Training Time (Minutes) and Overheads Across

| Model | Dataset | Full<br>Enc | Partly Enc |
|-------------|-------------|-------------|------------|
| | | (min) | (min) |
| | CIFAR-10 | 111 | 21 |
| | CT Kidney | 228 | 127 |
| EffNetB0 | Lung | 355 | 254 |
| | COVID | 698 | 591 |
| | Diabetic | 1298 | 1351 |
| | Retinopathy | | |
| | CIFAR-10 | 219 | 35 |
| | CT Kidney | 514 | 326 |
| DenseNet121 | Lung | 506 | 312 |
| | COVID | 1542 | 1351 |
| | Diabetic | 1542 | 1351 |
| | Retinopathy | | |
| | CIFAR-10 | 68 | 15 |
| | CT Kidney | 163 | 100 |
| MobileNetV2 | Lung | 467 | 231 |
| | COVID | 610 | 555 |
| | Diabetic | 610 | 555 |
| | Retinopathy | | |
| ResNet-50 | CIFAR-10 | 530 | 68 |
| | CT Kidney | 861 | 399 |
| | Lung | 834 | 372 |
| | COVID | 1140 | 673 |
| | | | |
| | Diabetic | 1140 | 673 |

![](_page_9_Figure_20.jpeg)
<!-- Image Description: The image displays a line graph showing the file size (in MB) of four different deep learning models (EfficientNetB0, DenseNet121, MobileNetV2, ResNet50) as a function of encryption percentage. The graph illustrates how the file size increases linearly with the percentage of encryption applied to each model, with ResNet50 showing the most significant size increase. The purpose is to compare the impact of encryption on the size of different model architectures. -->

Figure 8 Encrypted file size per encryption level (10% - 100%)

![](_page_9_Figure_22.jpeg)
<!-- Image Description: The image is a line graph showing the accuracy of four different convolutional neural networks (DenseNet, ResNet, EfficientNet, MobileNet) at varying levels of data encryption (0-90%). The x-axis represents the encryption percentage, and the y-axis represents the model accuracy. The graph illustrates how the accuracy of each model decreases as the encryption percentage increases. It likely demonstrates the impact of data encryption on model performance. -->

Figure 9 Accuracy Vs Encryption Percentage Across Different Models

### 7 Effects on Security

Before conducting our main security experiments, we implemented several security tests to evaluate the

![](_page_10_Figure_1.jpeg)
<!-- Image Description: The bar chart displays the encryption overhead (in minutes) for four different convolutional neural network models: EfficientNetB0, DenseNet121, MobileNetV2, and ResNet50. Two overheads are compared: Fully Homomorphic Encryption (blue bars) and FAS (red bars). The chart shows that ResNet50 has the highest Fully Homomorphic Encryption overhead (510 minutes), while EfficientNetB0 has the lowest (100 minutes). FAS overhead is significantly lower for all models. The chart visually compares the computational costs of the encryption methods across different model complexities. -->

Figure 10 Training Time and Encrypted Size Comparison for FHE and FAS Models (CT Kidney dataset)

Table 2 FHE vs FAS: Security Test Results

| Test | FAS | FHE |
|--------------------------|-------|-------|
| Integrity Check | False | False |
| Chosen-Plaintext Attack | True | True |
| Chosen-Ciphertext Attack | True | True |
| Noise and Precision Test | True | True |
| Timing Attack Test | True | True |
| Differential Attack Test | True | True |
| Statistical Dist. Test | True | True |
| Homomorphism Test | True | True |
| Leakage Test | True | True |

robustness of our encryption methods. These tests included integrity checks, timing attack tests, noise and precision evaluations, and simulations of chosenciphertext and chosen-plaintext attacks. Additional differential attack tests and statistical distribution checks were performed to verify that encryption preserved data integrity and privacy. Our findings indicate that 10% FAS encryption successfully passed the same security tests as 100% FHE, demonstrating strong security with reduced computational overhead.

Table 2 compares FAS with FHE across a series of security evaluations. The results confirm that FAS provides comparable protection, reinforcing its viability as a lightweight yet effective security mechanism.

### 7.1 Evaluating Privacy with MSSIM and VIFP

Model inversion attacks pose a threat to FL by reconstructing training data from model updates. To assess privacy resilience, we use Mean Structural Similarity Index (MSSIM) and Visual Information Fidelity in the Pixel domain (VIFP).

MSSIM quantifies structural similarity between original and reconstructed images, with lower scores indicating stronger privacy. VIFP measures visual quality based on perceptual models, highlighting the impact of noise and scrambling techniques. Both metrics are widely recognized for privacy evaluation in adversarial scenarios.

![](_page_10_Figure_10.jpeg)
<!-- Image Description: The image presents a line graph comparing the performance of four different convolutional neural networks (EfficientNetB0, DenseNet121, MobileNetV2, ResNet50) under varying levels of encryption. The x-axis represents the encryption percentage (0-90%), while the y-axis shows two performance metrics: MSSIM (structural similarity index) and VIFP (visual information fidelity). The graph illustrates how these metrics decrease as the encryption percentage increases for each network, indicating a degradation in image quality with higher encryption. -->

Figure 11 MSSIM and VIFP Scores across Encryption Percentages for Various Models

Our results show that selective encryption with scrambling and noise significantly degrades reconstruction quality. MSSIM stabilizes at 52% for 20% encryption, and VIFP follows a similar trend across multiple encryption levels. This confirms that our approach effectively mitigates inversion attacks while optimizing computational efficiency.

Further tests demonstrated that even at 10% encryption, reconstructed images showed significant distortion. The MSSIM score at 10% encryption was 58%, highlighting a substantial deviation from the original images. As encryption increased, the score stabilized at around 52%, reinforcing the effectiveness of partial encryption in maintaining privacy.

Figure 11 illustrates MSSIM and VIFP scores across encryption percentages for various models. Results were averaged across multiple runs to account for variations introduced by selective encryption, scrambling, and noise. The sharp decline in scores at 10% encryption, with stabilization around 20%, suggests that lower encryption levels can provide security equivalent to full encryption while significantly reducing computational costs. Notably, resistance to inversion attacks at 100% encryption is nearly identical to that at 10% and 20%, highlighting the robustness of selective encryption.

### 8 Cross-testing with Related Work

### 8.1 Comparison with MASKCRYPT

MASKCRYPT [19] applies a gradient-guided encryption mask to selectively encrypt critical model weights, reducing communication overhead by up to 4.15× compared to full model encryption. However, its gradient mask is not always optimized for selecting the most sensitive gradients, leading to lower initial security scores. MASKCRYPT requires multiple rounds to stabilize en-

![](_page_11_Figure_1.jpeg)
<!-- Image Description: The image displays a line graph comparing MSSIM and VIFp scores across three methods (FedML-HE, MaskCrypt, FAS) at varying encryption levels (0-90%). MSSIM and VIFp, likely image quality metrics, are plotted against encryption percentage. The graph shows how these metrics decrease with increasing encryption for each method, allowing for a performance comparison. -->

Figure 12 Comparison of MSSIM and VIFP Scores: FAS vs. FedML-HE vs. MASKCRYPT

cryption, as reflected in VIFP scores, which only stabilize by round 5. This indicates an adaptation period where security is suboptimal.

In contrast, FAS stabilizes earlier by combining selective homomorphic encryption, differential noise, and bitwise scrambling, encrypting a fixed percentage of weights without gradient sensitivity analysis or pretraining. This approach reduces processing time by 90% compared to FHE while maintaining strong resistance to model inversion attacks. Unlike MASKCRYPT, which recalculates sensitivity masks each round, FAS eliminates extra computational costs and scales effectively across federated networks.

### 8.2 Comparison with FedML-HE

FedML-HE [18] identifies and encrypts critical weights based on gradient sensitivity through a pre-training phase. Our recreated FedML-HE model provides insight into its behavior, though results may differ from the original implementation. While FedML-HE offers strong privacy protection, its pre-training phase introduces significant time and resource costs. Each client generates an encryption mask independently, which, while avoiding direct mask sharing, can lead to inconsistencies in aggregated model accuracy.

Our FAS method eliminates the need for pretraining and mask aggregation by encrypting a fixed percentage of weights with differential noise and bitwise scrambling. At 10% encryption, FAS achieves a MSSIM score of 58%, comparable to FedML-HE's 52%, but with significantly lower computational costs. The lack of pre-training and per-client mask generation allows FAS to maintain efficiency and scalability in FL environments.

Figure 12 compares FAS, FedML-HE, and MASKCRYPT across MSSIM and VIFP scores. At 10% encryption, FedML-HE shows slightly higher stability (MSSIM 52%), while FAS achieves 58%,

Table 3 Comparison of Encryption Techniques for Different Models

| Method | Model | Non | Total | Overhead |
|-----------|-------------|-----|-------|----------|
| | | Enc | (m) | (m) |
| FAS | EffNetB0 | 56 | 69 | 13 |
| FEDML-HE | EffNetB0 | 56 | 99 | 43 |
| MASKCRYPT | EffNetB0 | 56 | 89 | 33 |
| FAS | DenseNet121 | 152 | 176 | 24 |
| FEDML-HE | DenseNet121 | 152 | 210 | 58 |
| MASKCRYPT | DenseNet121 | 152 | 200 | 48 |
| FAS | MobileNetV2 | 46 | 52 | 6 |
| FEDML-HE | MobileNetV2 | 46 | 69 | 23 |
| MASKCRYPT | MobileNetV2 | 46 | 64 | 18 |
| FAS | ResNet-50 | 176 | 224 | 48 |
| FEDML-HE | ResNet-50 | 176 | 278 | 102 |
| MASKCRYPT | ResNet-50 | 176 | 246 | 70 |

and MASKCRYPT falls in between at 55%. As encryption increases to 20%, all methods converge with nearly identical security performance. Despite slight advantages for FedML-HE in lower encryption levels, FAS provides comparable security at significantly lower computational costs. MASKCRYPT's need for sensitivity mask recalculation each round makes it less efficient for real-time scenarios. These findings position FAS as an optimal choice for scalable, privacy-sensitive FL applications requiring low-latency performance.

Table 3 compares non-encrypted, partly encrypted, and overhead times for different models using FAS, FedML-HE, and MASKCRYPT on the Kidney dataset. The values are reconstructed based on methodologies described in the respective papers. FAS consistently has the lowest overhead across models, making it the most efficient. FedML-HE has the highest overhead due to pre-training, while MASKCRYPT offers a balance but initially has lower security, improving after multiple rounds. Overall, FAS is the best option for efficiency and scalability in FL.

## 9 Comparative Analysis of Encryption Techniques Across Datasets

This section compares the performance of FAS, FEDML-HE, and MASKCRYPT across five datasets: CIFAR-10, Diabetic Retinopathy, COVID, Lung, and Kidney. The analysis highlights FAS's efficiency in minimizing overhead and encryption time compared to the other methods.

Across all datasets, FAS consistently achieves the lowest training times and computational overhead as we can see from Figures 13, 14, 17, 16, 15. Unlike FEDML-HE, which incurs significant pretraining costs for sensitivity mask creation, and MASKCRYPT, which generates masks at each round, FAS employs a

![](_page_12_Figure_1.jpeg)
<!-- Image Description: The bar chart compares the execution times (in minutes) of different encrypted deep learning models (EffNetB0, DenseNet121, MobileNetV2, ResNet-50) using various encryption techniques: FAS, MASKCRYPT, and FEDML-HE. Each bar is segmented to show the encrypted computation time and the overhead for each method. A "Fully Encrypted" control group is included for comparison. The chart illustrates the performance trade-offs between different privacy-preserving machine learning approaches. -->

Figure 13 Comparison of Partly Encrypted and Fully Encrypted Metrics Across Models (CIFAR-10).

![](_page_12_Figure_3.jpeg)
<!-- Image Description: The bar chart displays the encrypted inference time (in minutes) for four different deep learning models (EffNetB0, DenseNet121, MobileNetV2, ResNet-50) using three different secure inference methods (FAS, FEDML-HE, MASKCRYPT) and a fully encrypted control. Each bar is segmented to show the encrypted computation time and the overhead of each method. The gray bars represent the fully encrypted control, showcasing the total time. The chart compares the performance and overhead of the secure inference techniques across various model architectures. -->

Figure 14 Comparison of Partly Encrypted and Fully Encrypted Metrics Across Models (Diabetic Retinopathy).

random masking strategy with minimal computation. This advantage is particularly evident in lightweight models like MobileNetV2 on the COVID dataset and larger models like ResNet-50 on the Lung dataset. The efficiency of FAS is further demonstrated in the Diabetic Retinopathy and Kidney datasets, where it eliminates pretraining and per-round computations, making it the most practical and scalable approach. Overall, FAS outperforms the other techniques across all datasets, confirming its robustness and adaptability.

Figures 13, 15, 14, 17 and 16 shows that across all datasets, FAS consistently outperforms FEDML-HE and MASKCRYPT in terms of total training time and overhead. The absence of sensitivity mask pretraining or extra per-round computations is the key factor contributing to its superior performance. These results establish FAS as the optimal choice for applications requiring fast and efficient encryption without compro-

![](_page_12_Figure_7.jpeg)
<!-- Image Description: This grouped bar chart compares the training times (in minutes) of four convolutional neural networks (EffNetB0, DenseNet121, MobileNetV2, ResNet-50) under different privacy-preserving training methods. Each bar represents a model trained with either fully encrypted methods (control), FAS, or FEDML-HE, showing the encrypted computation time and the overhead introduced by each method. The chart visualizes the trade-off between security and training efficiency for these models. -->

Figure 15 Comparison of Partly Encrypted and Fully Encrypted Metrics Across Models (COVID).

![](_page_12_Figure_9.jpeg)
<!-- Image Description: This bar chart compares the training times (in minutes) of four different deep learning models (EffNetB0, DenseNet121, MobileNetV2, ResNet-50) under various secure training protocols: FAS, MASKCRYPT, and FEDML-HE. Each protocol's encrypted and overhead times are shown separately. A "Fully Encrypted" control group is included for comparison. The chart illustrates the relative performance and overhead of different secure training methods across various model architectures. -->

Figure 16 Comparison of Partly Encrypted and Fully Encrypted Metrics Across Models (Lung).

![](_page_12_Figure_11.jpeg)
<!-- Image Description: The image presents a grouped bar chart comparing the computation times (in minutes) of five different deep learning models (EffNetB0, DenseNet121, MobileNetV2, ResNet-50) under various secure computation schemes: FAS, MASKCRYPT, and FEDML-HE. Each model's bar is segmented to show the encrypted computation time and the overhead for each scheme. A "Fully Encrypted (Control)" bar represents a baseline. The chart illustrates the performance trade-offs between different secure computation methods in terms of computation time for various model architectures. -->

Figure 17 Comparison of Partly Encrypted and Fully Encrypted Metrics Across Models (Kidney).

mising security. We can see that in smaller datasets which training time is not significant, difference between encryption technique becomes more obvious.

Table 4 Top 3 Cases Where FAS Outperforms Other Models

| Dataset Model | | Compared | Enc.<br>Impr.<br>(%) | Overhead<br>Impr.<br>(%) |
|---------------|-------------|---------------|----------------------|--------------------------|
| COVID | MobileNetV2 | FEDML<br>HE | 42.50 | 73.91 |
| COVID | EffNetB0 | FEDML<br>HE | 46.15 | 69.77 |
| COVID | EffNetB0 | MASK<br>CRYPT | 36.36 | 60.61 |

Table 4 presents the top three cases where the FAS encryption model demonstrates a higher efficiency compared to FEDML-HE and MASKCRYPT in terms of encryption time and overhead reduction.

COVID dataset with MobileNetV2: FAS achieves a 42.50% faster encryption time and a 73.91% lower overhead than FEDML-HE. COVID dataset with EffNetB0: FAS provides a 46.15% encryption improvement and a 69.77% overhead reduction compared to FEDML-HE. COVID dataset with EffNetB0 (vs. MASKCRYPT): FAS reduces encryption time by 36.36% and overhead by 60.61%. These results suggest that FAS is particularly effective in reducing computational overhead while maintaining faster encryption speeds, especially in the COVID dataset with lightweight models.

## 10 Handling Data Skew in Encryption-Based Techniques

This section investigates how data skew affects different encryption techniques, with an emphasis on evaluating the robustness of the proposed FAS approach in comparison to existing methods like MASKCRYPT and Fedml-HE.

## 10.1 Challenges with Mask-Based Techniques

Both MASKCRYPT and Fedml-HE rely on sensitive masks to select important gradients for encryption. that strongly affect how well the model performs. However, in scenarios with skewed data distributions, the importance of gradients becomes difficult to determine accurately. As a result, the encryption decisions made by these methods often degrade to levels resembling random encryption. This reduces their effectiveness, as observed in the MSSIM and VIFP score comparisons.

### 10.2 Robustness of the FAS Technique

In contrast, the proposed FAS technique, which operates as a random encryption method, is unaffected by data skew. Unlike mask-based techniques, FAS does not depend on the model's accuracy or gradient importance for its encryption process. Instead, it employs a combination of encryption, scrambling, and noise addition. These components ensure that the method maintains consistent performance irrespective of the underlying data distribution. The robustness of this approach makes it particularly suitable for scenarios where data skew is prevalent, such as FL environments with heterogeneous clients.

### 10.3 Experimental Results and Comparisons

| Dataset | Method | MSSIM<br>(Skew/<br>Normal) | VIFP<br>(Skew/<br>Normal) |
|-------------|-----------|----------------------------|---------------------------|
| | Fedml-HE | 63 / 57 | 18 / 13 |
| Kidney | FAS | 62 / 61 | 16.5 / 15 |
| | MASKCRYPT | 63 / 60 | 18 / 15 |
| | Control | 70 / 70 | 20 / 20 |
| | Fedml-HE | 65 / 59 | 19 / 14 |
| Lung | FAS | 62 / 61 | 16.5 / 15 |
| | MASKCRYPT | 66 / 62 | 19 / 16 |
| | Control | 70 / 70 | 20 / 20 |
| | Fedml-HE | 66 / 60 | 20 / 15 |
| | FAS | 62 / 61 | 16.5 / 15 |
| COVID | MASKCRYPT | 67 / 63 | 20 / 17 |
| | Control | 70 / 70 | 20 / 20 |
| | Fedml-HE | 64 / 58 | 18 / 14 |
| Diabetic | FAS | 62 / 61 | 16.5 / 15 |
| Retinopathy | MASKCRYPT | 65 / 61 | 19 / 16 |
| | Control | 70 / 70 | 20 / 20 |
| | Fedml-HE | 62 / 58 | 17 / 13 |
| | FAS | 61 / 59 | 16.5 / 15 |
| CIFAR-10 | MASKCRYPT | 64 / 59 | 18 / 14 |
| | Control | 70 / 70 | 20 / 20 |

Table 5 MSSIM and VIFP Scores for Skew and Normal Data across Datasets

Table 5 demonstrates that the proposed FAS technique, leveraging encryption, scrambling, and noise, exhibits superior robustness to data skew across all evaluated datasets—Kidney, Lung, COVID, and Diabetic Retinopathy—when compared to existing gradientbased encryption methods. This characteristic ensures that FAS maintains its performance and security advantages even in diverse, real-world scenarios with varying data distributions. Experimental results using the Effi-

![](_page_14_Figure_1.jpeg)
<!-- Image Description: The image displays a line graph comparing the accuracy of several federated learning methods (FAS, MASKCRYPT, Fedml-HE) across different deep learning models (EfficientNet, DenseNet, ResNet, MobileNet). Accuracy is shown for both "normal" and "skew" data distributions. The graph shows how accuracy varies across models and methods, with accuracy generally decreasing as model complexity (from EfficientNet to MobileNet) increases. The purpose is to illustrate the comparative performance of the different federated learning approaches under varying conditions. -->

Figure 18 Effect of Data Skew on CIFAR Dataset Across Different Techniques

cientNetB0 model across these datasets show that the accuracy of FAS is minimally affected by data skew, while other methods experience significant performance degradation under similar conditions. These findings highlight the adaptability and reliability of the FAS technique in privacy-preserving machine learning applications.

- For MASKCRYPT and Fedml-HE, the MSSIM and VIFP scores under skewed data are significantly degraded, closely resembling random encryption.
- In contrast, the FAS technique maintains reduced degragation across all conditions, as its random encryption approach is independent of the data distribution.
- The control value has been kept same with skewed and normal to show the random selective encryption comparison.

### Effect of Data Skew on Training Performance

Figure 18 illustrates the uniform reduction in accuracy across three techniques—FAS, MASKCRYPT, and Fedml-HE—when training on skewed data using the CIFAR dataset. While all techniques show similar accuracy drops under skewed conditions, the implications for their security mechanisms differ significantly.

- MASKCRYPT and Fedml-HE: Both techniques rely on sensitivity masks to ensure data security. As training accuracy decreases under skewed conditions, the quality and reliability of these sensitivity masks are compromised, potentially leaving the system insecure until the mask stabilizes.
- FAS: Unlike the other techniques, FAS does not depend on sensitivity masks. This independence ensures that the MS-SSIM and VIFP scores of FAS remain stable, even when training on skewed data. The inherent robustness of FAS allows it to main-

tain its security guarantees regardless of data distribution.

These results highlight a critical advantage of FAS: its ability to decouple data security from training accuracy. While longer training epochs can partially recover accuracy for MASKCRYPT and Fedml-HE, their reliance on sensitivity masks introduces a window of vulnerability during the calibration phase. In contrast, FAS maintains consistent security and performance, making it a more robust choice under challenging data conditions.

### 7 Conclusion

This paper evaluated privacy-preserving techniques in FL, focusing on different datasets and comparing differential privacy, HE, and our custom FAS approach.

FHE offers the highest data protection but incurs significant computational costs, making it suitable only for scenarios prioritizing confidentiality over performance. Differential privacy provides lightweight privacy with minimal impact on computation, ideal for moderate security requirements. Our FAS method strikes a balance by achieving security comparable to full encryption while significantly reducing training time and overhead, making it efficient for large-scale FL and resource-constrained environments.

FAS's layered approach—combining selective encryption, bitwise scrambling, and differential noise—demonstrates strong resilience against model inversion attacks without requiring pre-training or complex mask aggregation, outperforming FedML-HE and MASKCRYPT in scalability and efficiency. FAS offers slighly better security compared to models that require accurate sensitivity masks for data skews or operate under general low-accuracy conditions.

In summary, FAS offers an effective middle ground, balancing security and performance for real-time, privacy-sensitive applications like healthcare. Future research will refine these techniques and explore hybrid approaches across diverse datasets and federated environments to enhance scalability and applicability.

### 8 Acknowledgments

The first author (A. K.) was supported by the Republic of T¨urkiye.

## References

1. Koneˇcn`y, Jakub and McMahan, H Brendan and Yu, Felix X and Richt´arik, Peter and Suresh, Ananda Theertha and Bacon, Dave, "Federated learning: Strategies for improving communication efficiency," arXiv preprint arXiv:1610.05492, 2016.

- 2. He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian, "Deep residual learning for image recognition," in Proceedings of the IEEE conference on computer vision and pattern recognition, 2016, pp. 770–778.
- 3. Huang, Gao and Liu, Zhuang and Van Der Maaten, Laurens and Weinberger, Kilian Q, "Densely connected convolutional networks," in Proceedings of the IEEE conference on computer vision and pattern recognition, 2017, pp. 4700– 4708.
- 4. Tan, Mingxing and Le, Quoc, "Efficientnet: Rethinking model scaling for convolutional neural networks," in International conference on machine learning, 2019, pp. 6105–6114.
- 5. Howard, Andrew G and Zhu, Menglong and Chen, Bo and Kalenichenko, Dmitry and Wang, Weijun and Weyand, Tobias and Andreetto, Marco and Adam, Hartwig, "Mobilenets: Efficient convolutional neural networks for mobile vision applications," arXiv preprint arXiv:1704.04861, 2017.
- 6. Kaggle, "Diabetic retinopathy detection," Kaggle, 2015. [Online]. Available: https://www.kaggle.com/competitions/ diabetic-retinopathy-detection/overview
- 7. Prashant Patel, "Chest X-ray (Covid-19 & Pneumonia)" Kaggle, 2020. [Online]. Available: https://www.kaggle.com/datasets/ prashant268/chest-xray-covid19-pneumonia
- 8. Larxel, "Lung and Colon Cancer Histopathological Images," Kaggle, 2020. [Online]. Available: https: //www.kaggle.com/datasets/andrewmvd/ lung-and-colon-cancer-histopathological-images
- 9. M. N. Islam, "CT Kidney Dataset: Normal-Cyst-Tumor and Stone," Kaggle, 2020. [Online]. Available: https: //www.kaggle.com/datasets/nazmul0087/ ct-kidney-dataset-normal-cyst-tumor-and-stone
- 10. Duplyakin, Dmitry and Ricci, Robert and Maricq, Aleksander and Wong, Gary and Duerig, Jonathon and Eide, Eric and Stoller, Leigh and Hibler, Mike and Johnson, David and Webb, Kirk and others, "The Design and Operation oaf Cloud-Lab," in 2019 USENIX annual technical conference (USENIX ATC 19), 2019, pp. 1–14.
- 11. Beutel, Daniel J and Topal, Taner and Mathur, Akhil and Qiu, Xinchi and Parcollet, Titouan and de Gusm˜ao, Pedro PB and Lane, Nicholas D,

"Flower: A friendly federated learning research framework," arXiv preprint arXiv:2007.14390, 2020.

- 12. Abadi, Mart´ın and Barham, Paul and Chen, Jianmin and others, "TensorFlow: a system for largescale machine learning," in 12th USENIX symposium on operating systems design and implementation (OSDI 16), 2016, pp. 265–283.
- 13. Paszke, Adam and Gross, Sam and Massa, Francisco and Lerer, Adam and Bradbury, James and Chanan, Gregory and Killeen, Trevor and Lin, Zeming and Gimelshein, Natalia and Antiga, Luca and others, "PyTorch: An imperative style, highperformance deep learning library," Advances in neural information processing systems, vol. 32, 2019.
- 14. Chen, Tianqi and Li, Mu and Li, Yutian and Lin, Min and Wang, Naiyan and Wang, Minjie and Xiao, Tianjun and Xu, Bing and Zhang, Chiyuan and Zhang, Zheng, "MXNet: A flexible and efficient machine learning library for heterogeneous distributed systems," arXiv preprint arXiv:1512.01274, 2015.
- 15. Dwork, Cynthia, "Differential Privacy," in Automata, Languages and Programming, 2006, pp. 1–12.
- 16. Gentry, Craig, "Fully homomorphic encryption using ideal lattices," Proceedings of the 41st annual ACM symposium on Theory of computing, pp. 169–178, 2009.
- 17. Boneh, Dan and Franklin, Matt, "Threshold decryption," in CRYPTO, 2006.
- 18. Jin, Weizhao and Yao, Yuhang and Han, Shanshan and Gu, Jiajun and Joe-Wong, Carlee and Ravi, Srivatsan and Avestimehr, Salman and He, Chaoyang, "FedML-HE: An Efficient Homomorphic-Encryption-Based Privacy-Preserving Federated Learning System," arXiv preprint arXiv:2303.10837, 2024. [Online]. Available: https://arxiv.org/abs/2303.10837
- 19. Hu, Chenghao and Li, Baochun, "MASKCRYPT: Federated Learning with Selective Homomorphic Encryption," IEEE Transactions on Dependable and Secure Computing, 2024.
- 20. Korkmaz, Abdulkadir and Alhonainy, Ahmad and Rao, Praveen, "An Evaluation of Federated Learning Techniques for Secure and Privacy-Preserving Machine Learning on Medical Datasets," in 2022 IEEE Applied Imagery Pattern Recognition Workshop (AIPR), 2022.
- 21. Wang, Zhou and Bovik, Alan C and Sheikh, Hamid R and Simoncelli, Eero P, "Image quality assessment: From error visibility to structural

similarity," IEEE Transactions on Image Processing, vol. 13, no. 4, pp. 600–612, 2004.

- 22. Sheikh, Hamid R and Bovik, Alan C and De Veciana, Gustavo, "Image quality assessment: From error visibility to structural similarity," IEEE Transactions on Image Processing, vol. 15, no. 2, pp. 430–444, 2006.
- 23. McMahan, H. Brendan and Moore, Eider and Ramage, Daniel and Hampson, Seth and Arcas, Blaise Ag¨uera y, "Communication-efficient learning of deep networks from decentralized data," in Artificial intelligence and statistics, 2017, pp. 1273–1282.
- 24. Yang, Xiaoyu and Li, Wei and Zhang, Ping, "Bitwise scrambling: A secure and efficient obfuscation technique for data protection," in 2017 IEEE Conference on Communications and Network Security (CNS), 2017, pp. 1–9.
- 25. Fan, Junfeng and Vercauteren, Frederik, "Somewhat practical fully homomorphic encryption," IACR Cryptology ePrint Archive, vol. 2012, pp. 144, 2012.
- 26. Chillotti, Ilaria and Gama, Nicolas and Georgieva, Mariya and Izabach`ene, Malo, "Faster fully homomorphic encryption: Bootstrapping in less than 0.1 seconds," in International Conference on the Theory and Application of Cryptology and Information Security, 2016, pp. 3–33.
- 27. Ducas, L´eo and Micciancio, Daniele, "FHEW: Bootstrapping homomorphic encryption in less than a second," in Annual International Conference on the Theory and Applications of Cryptographic Techniques, 2015, pp. 617–640.
- 28. Brakerski, Zvika and Vaikuntanathan, Vinod, "Efficient Fully Homomorphic Encryption from (Standard) LWE," in 2011 IEEE 52nd Annual Symposium on Foundations of Computer Science, 2011, pp. 97–106.
- 29. Cheon, Jung Hee and Kim, Andrey and Kim, Miran and Song, Yongsoo, "Homomorphic encryption for arithmetic of approximate numbers," in International Conference on the Theory and Application of Cryptology and Information Security, 2017, pp. 409–437.
- 30. Dwork, Cynthia and McSherry, Frank and Nissim, Kobbi and Smith, Adam, "Calibrating noise to sensitivity in private data analysis," in Theory of Cryptography Conference, 2006, pp. 265–284.
- 31. Abadi, Martin and Chu, Andy and Goodfellow, Ian and McMahan, H Brendan and Mironov, Ilya and Talwar, Kunal and Zhang, Li, "Deep learning with differential privacy," in Proceedings of the 2016 ACM SIGSAC conference on computer and

communications security, 2016, pp. 308–318.

- 32. Wu, Xiuwen and Kumar, Anil and Qin, Xin and Wang, Hui and Xu, Kun and Xiong, Hui, "Towards privacy-preserving federated learning," in Proceedings of the 28th ACM International Conference on Information and Knowledge Management, 2019, pp. 1817–1826.
- 33. Smart, Nigel P and Vercauteren, Frederik, "Fully Homomorphic Encryption with Relatively Small Key and Ciphertext Sizes," Springer, 2014.
- 34. Chillotti, Ilaria and Gama, Nicolas and Georgieva, Mariya and Izabach`ene, Malo, "Faster Fully Homomorphic Encryption: Bootstrapping in Less Than 0.1 Seconds," in International Conference on the Theory and Application of Cryptology and Information Security, 2018, pp. 3–33.
- 35. Mironov, Ilya, "R´enyi Differential Privacy," IEEE Computer Security Foundations Symposium, pp. 263–275, 2017.
- 36. Cheon, Jung Hee and Gentry, Craig and Halevi, Shai and Smart, Nigel P, "Bootstrapping for Approximate Homomorphic Encryption," Springer, 2018.
- 37. Li, Tian and Sahu, Anit Kumar and Talwalkar, Ameet and Smith, Virginia, "Privacy-Preserving Federated Learning: Challenges, Methods, and Future Directions," arXiv preprint arXiv:1909.06335, 2019.
- 38. Song, Congzheng and Ristenpart, Thomas and Shmatikov, Vitaly, "Privacy-Preserving Deep Learning via Additively Homomorphic Encryption," arXiv preprint arXiv:1706.09871, 2020.
- 39. Halevi, Shai and Halevi, Tian and Jeffrey, Halevi, "Faster Homomorphic Encryption: Bootstrapping in Less Than a Second," in ACM Conference on Computer and Communications Security (CCS), 2019, pp. 3–33.
- 40. Ma, Xiaoyu and Chen, Xinyu and Ma, Chuan, "Secure Aggregation for Federated Learning with Differential Privacy," IEEE Transactions on Network and Service Management, pp. 345–359, 2020.
- 41. Xu, Zhen and Yang, Xiaoyan and Liu, Qian and Zheng, Tao and Jiang, Xiao, "HybridAlpha: An Efficient Privacy-Preserving Federated Learning System," IEEE Transactions on Network and Service Management, pp. 123–137, 2019.
- 42. C. Dwork and A. Roth, "The algorithmic foundations of differential privacy," Foundations and Trends in Theoretical Computer Science, vol. 9, no. 3-4, pp. 211–407, 2014.
- 43. C. Dwork, F. McSherry, K. Nissim, and A. Smith, "Calibrating noise to sensitivity in private data analysis," in Theory of Cryptography Conference

(TCC), 2006, pp. 265–284.

- 44. C. Fontaine and F. Galand, "A survey of homomorphic encryption for nonspecialists," EURASIP Journal on Information Security, vol. 2007, no. 1, pp. 1–10, 2007.
- 45. C. Zhang, S. Li, J. Kang, X. Wang, F. Li, and Y. Liu, "BatchCrypt: Efficient homomorphic encryption for cross-silo federated learning," in USENIX Annual Technical Conference (USENIX ATC), 2020, pp. 493–506. [Online]. Available: https://www.usenix.org/conference/atc20/ presentation/zhang-chengliang
- 46. A. Krizhevsky, "Learning multiple layers of features from tiny images," Technical Report, University of Toronto, 2009.


## TL;DR
Research on a selective homomorphic encryption approach for faster privacy-preserving federated learning providing insights for knowledge graph development and data integration.

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