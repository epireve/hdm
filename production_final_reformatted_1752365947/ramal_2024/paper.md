---
cite_key: ramal_2024
title: A Hybrid Optimization and Machine Learning Framework for Urban Traffic Management Using Cyber-Physical Digital Twin Architecture
authors: India janakiramal, India eanbalagan
year: 2024
doi: 10.1109/TEM.2024.3520255
url: https://ieeexplore.ieee.org/document/10983125/
relevancy: Medium
tldr: Hybrid optimization framework using digital twins for urban system management
insights: CPDT architecture integrates PSO and ABC algorithms with Transformer networks achieving 20% reduction in traffic delays and 15% prediction accuracy increase
summary: This paper develops a Cyber-Physical Digital Twin (CPDT) architecture integrating data from multiple sources using hybrid optimization combining Particle Swarm Optimization, Artificial Bee Colony algorithms, and Transformer networks
research_question: How can advanced technologies improve urban traffic management and reduce congestion?
methodology: CPDT architecture, hybrid PSO-ABC optimization, Transformer networks for prediction, multi-source data integration
key_findings: 20% reduction in average traffic delays, 15% increase in prediction accuracy, demonstrated effective hybrid optimization approach
limitations: Limited to traffic management domain, computational complexity not discussed
conclusion: Shows promise for intelligent system optimization using advanced computational techniques
future_work: Apply to personal schedule optimization, integrate with HDM planning systems, develop user-friendly interfaces
implementation_insights: Agent Epsilon: Hybrid optimization techniques applicable to HDM predictive modeling and resource optimization
tags: 
standardization_date: 2025-07-10
standardization_version: 1.0
---

# A Hybrid Optimization and Machine Learning Framework for Urban Traffic Management Using Cyber-Physical Digital Twin Architecture

P.Janaki Ramal *Research Scholar, Department of CSE, Saveetha School of Engineering, Saveetha Institute of Medical and Technical Sciences* Thandalam, Chennai, Tamilnadu, India janakiramal424@gmail.com

*Abstract —* **As cities continue to expand rapidly, traffic congestion has become a pressing issue, necessitating advanced traffic management systems. This research proposes a Cyber-Physical Digital Twin (CPDT) architecture for optimizing urban traffic and simulating smart city transportation systems in real-time. The CPDT framework integrates data from various sources to provide a dynamic and real-time overview of city traffic. In this enhanced approach, a hybrid methodology combining Particle Swarm Optimization (PSO) and Artificial Bee Colony (ABC) algorithms is utilized to optimize both route planning and traffic signal timings. Additionally, advanced machine learning model Transformer networks are employed to forecast traffic patterns and incidents. These improvements lead to a 20% reduction in average traffic delays and a 15% increase in prediction accuracy, thereby enhancing traffic management outcomes and overall prediction reliability.**

## TL;DR
Hybrid optimization framework using digital twins for urban system management

## Key Insights
CPDT architecture integrates PSO and ABC algorithms with Transformer networks achieving 20% reduction in traffic delays and 15% prediction accuracy increase

*Keywords— smart traffic management, data collection, machine learning, traffic prediction, real-time analysis, system adaptation, signal optimization.*

## I. INTRODUCTION

The emergence of urban traffic congestion as a critical issue in modern cities has been influenced by a combination of factors, including vehicles increasing on the road, rapid urbanization, and a growing population [[1]](#ref-1). Financial losses, pollution, and delays are all consequences of the increasing complexity of maintaining transportation networks as a result of urbanization [[2]](#ref-2). Public transportation, logistics, and the daily activities of individuals are adversely affected by congestion. These problems are more severe in densely populated areas because the road infrastructure is insufficient to accommodate the increasing volume of traffic [[3]](#ref-3). In order to address these obstacles, new technologies must be implemented that are capable of facilitating real-time traffic flow control and eliminating bottlenecks. Traditional methods, including static route design, manually monitoring road conditions, and fixed-time traffic signal regulation, have been employed for a long time to regulate city traffic [[4]](#ref-4). These systems accomplish their objectives; however, they are inadequately equipped to manage traffic patterns that are susceptible to fluctuations in real time, as they are predicated on predetermined parameters. Road capacity is underutilized or delays occur when fixed signal timings fail to adjust to changing traffic volumes throughout the day [[5]](#ref-5). In the same way that drivers are provided with itineraries by static route planning systems, which do not adjust to unanticipated events

E.Anbalagan Professor, *Department of CSE, Saveetha School of Engineering, Saveetha Institute of Medical and Technical Sciences* Thandalam, Chennai, Tamilnadu, India eanbalagan77@gmail.com

such as accidents, road closures, or traffic, these may also lead to less-than-ideal travel times. The ineffectiveness of manual traffic monitoring is a result of human error [[6]](#ref-6); it may overlook significant traffic patterns and take an excessive amount of time to respond to unforeseen changes.

These traditional methods are insufficient for contemporary urban development due to three critical factors: adaptability, efficiency, and scalability. The proliferation of real-time data from sources such as GPS devices, traffic cameras, and Internet of Things sensors, in conjunction with the increasing complexity of transportation systems, presents an opportunity to create more adaptive and intelligent traffic management solutions. The utilization of this data in real-time has the potential to enhance transportation efficacy, alleviate congestion, and optimize traffic flow. A system that is capable of real-time data processing and prediction, and that is integrated into a broader framework that can manage operations throughout the city, is necessary for this. The objective of this project is to enhance the management of traffic by utilizing the Cyber-Physical Digital Twin (CPDT) architecture to model and optimize urban traffic systems in real-time. The framework's capacity to offer a real-time representation of the city's traffic is based on a variety of sources, such as traffic cameras, IoT sensors, and GPS devices. The system employs a hybrid optimization approach that integrates Artificial Bee Colony (ABC) [[7]](#ref-7) algorithms with Particle Swarm Optimization (PSO) [[8]](#ref-8) to improve traffic flow and reduce congestion. These algorithms optimize traffic signal timings and route planning, which is a critical aspect of traffic management. The system becomes more responsive and effective by predicting traffic patterns and challenges through the use of machine learning techniques, particularly Transformer networks. The proposed methodology will integrate traditional traffic management methods with more contemporary data-driven alternatives. The CPDT framework provides a more adaptable and scalable approach to the management of urban traffic, the reduction of congestion, and the enhancement of the overall efficacy of municipal transportation systems by responding to real-time conditions. A novel approach to city traffic management has been introduced in the integration of optimization algorithms and ML models into the CPDT architecture. This approach is capable of accommodating the dynamic nature of urban traffic.

## II. LITERATURE REVIEW

To maximize signal timings, mitigate accidents, and improve traffic flow, urban traffic management has implemented modern technologies such as AI, ML, and the IoT. These sophisticated technologies are being employed because conventional methods are incapable of managing the intricacies of contemporary urban traffic. A machine-learning approach was developed by Gupta et al. [[10]](#ref-10) to modify the timing of traffic signals by incorporating real-time data, including vehicle counts and speeds. Their algorithms were so adept at anticipating areas with high traffic that they significantly reduced both pollution and travel times. In theory, however, the integration of autonomous vehicles with ML-based traffic systems would result in significantly higher yields. Additionally, Kumar et al. [[11]](#ref-11) investigated the feasibility of forecasting traffic volumes on Hyderabad's Nizampet road by employing ANN in conjunction with Support Vector Regression (SVR). The SVR model was entirely surpassed by the ANN model in terms of prediction accuracy. The study's method's viability must be questioned as a result of its restricted geographic scope. M.C. et al. [[9]](#ref-9) developed an AI-driven system for traffic signal management that leverages the cloud, the Internet of Things (IoT), and congestion alleviation algorithms, building upon their previous research in traffic optimization. The system enhanced traffic control, among other things, by collecting and analyzing data in real-time. However, their algorithms were too intricate and incapable of scaling, which prevented them from expanding their use in urban areas. A networked computing-at-the-edge-based adaptive traffic signal control system was investigated by S. et al. [[13]](#ref-13). Despite the fact that their decentralized approach enhanced computational efficiency, they encountered difficulties managing unanticipated traffic surges during emergencies. More precise traffic monitoring has been made possible by forthcoming advancements in computer vision. A neural network (NN) based video traffic surveillance system (VTSS) was devised by Bindu Madhavi et al. [[12]](#ref-12). This method was able to attain a 93% success rate in accident detection. This work underscores the potential of CNNs to improve real-time traffic control; however, there are still open concerns regarding scalability and dispersion across cities. Transformer-based models are a game-changer in traffic forecasting, as they are capable of capturing long-range dependencies. Their forecasts are exceedingly precise. In comparison to other conventional models, such as conventional recurrent neural networks and convolutional neural networks, the Time-Fusion Transformer model's [[15]](#ref-15) capacity to efficiently process historical traffic data is particularly noteworthy. By learning traffic patterns throughout the year, transformers have the potential to improve prediction models, which is why researchers are contemplating their use in urban traffic control. Chaudhari et al. [[14]](#ref-14) investigated the use of ML models, specifically deep learning algorithms, to forecast traffic flows at crossings in order to implement adaptive traffic control. They found that MLPNNs are more accurate in their predictions than RNNs, which could provide new opportunities for optimizing traffic flow at complex crossings. Parvathy et al. [[16]](#ref-16) conducted an investigation into intelligent traffic control by combining deep learning with IoT devices. The integration of a variety of data sources was a challenge when neural networks were employed in conjunction with sensor data, despite the fact that traffic flow projections were enhanced. Additionally, Govindaraj et al. [[17]](#ref-17) investigated hybrid AI models to optimize traffic routing, with an emphasis on the potential for ML-based adaptive routing systems to mitigate petroleum consumption. Despite their enhanced overall performance, the models' traffic control capabilities were deficient in densely populated regions. J. et al. [[18]](#ref-18) introduced a hybrid system that optimizes traffic management by combining traffic signal control with reinforcement learning. Even if this technology has been effective in simulations, it must undergo additional validation in real-world scenarios before it can be employed to dynamically adjust signal timings using traffic flow data.

## III. METHODOLOGY

## *A. Data Collection*

To optimize traffic signals and respond to real-time events, urban traffic management systems must collect data instantaneously. The primary instruments for collecting traffic data in this investigation were Google Maps and its associated SDKs and APIs. The exhaustive collection of capabilities available in Google Maps enables the collection of accurate and comprehensive traffic data from multiple locations, thereby enabling the construction of a robust dataset for urban traffic analysis. Google Maps API analyzes factors such as traffic volumes, velocities, and congestion levels to provide traffic data that is current. It also utilizes data collected from GPS-enabled devices such as cellphones, as well as data from public transportation networks and third-party service providers. The traffic layer of Google, which processes and provides access to this aggregated data, was employed to monitor traffic density at critical city intersections in this research. We employed a variety of Google Maps services to ensure that we obtained all the necessary information. The dynamic integration of real-time traffic data into the framework was enabled by the Maps SDK for Web and Android platforms, which enabled the traffic signal control system to acquire the most recent information on traffic conditions. By incorporating 360-degree street-level photography into the Street View API, additional data elements, including lane counts and road conditions, were incorporated. This data was indispensable for the calibration of traffic models, as it disclosed the width of roadways, the utilization of lanes, and other infrastructure features that influence traffic flow. The Elevation API was employed to account for the road gradients, as variations in elevation could potentially affect the speeds of vehicles and traffic. Information regarding traffic volumes and the scheduling of signals at significant crossings was a critical component of the data set. This is made possible by the integration of data from Google Maps Datasets, which enables the downloading, organization, and storage of substantial volumes of traffic data for future research. For a period of several weeks, we observed the flow of traffic, noting both periods of high and low volume. The data set contained data regarding the number of vehicles, average speeds, wait periods at traffic signals, and the durations of the green, yellow, and red phases. The data was categorized into databases based on attributes such as traffic volumes, intersection identification, time markers, and signal timing settings. In order to supplement the dataset with additional variables, such as environmental factors like weather conditions, we utilized secondary data sources. The collection encompasses specific points of interest, including accident-prone zones, through the utilization of the Google Maps Static Maps API. Additionally, the Aerial View API was employed to generate video visualizations of traffic patterns, which provided a bird's-eye perspective on the evolution of congestion over time. These visual insights enabled us to more effectively identify traffic bottlenecks and enhance traffic signals. After data collection, all items were preprocessed and organized to ensure consistency and usability. Outliers were eliminated through data cleaning techniques, which included abnormalities in the number of vehicles during nonoperational hours. After cleansing the dataset, we normalized it and interpolated any missing data points that were required. Some of the main variables that were incorporated into the final, clean dataset that was generated for transportation flow management were vehicle speeds, road conditions, signal timings, and volume. This enabled the efficient management of traffic signals. With the assistance of a clean, preprocessed dataset and precise insights into traffic patterns, the hybrid traffic management system that was proposed was more effectively developed. Table 1 shows the description about the dataset attributes.

| Attribute | Description |
|---|---|
| Intersection ID | Identifier for each traffic intersection. |
| Timestamp | Date and time of data collection, allowing for analysis of traffic patterns over time. |
| Vehicle Count | Vehicles passing through the intersection during a specified time interval. |
| Average Speed | Average speed of vehicles in km/h for the intersection during the specified time interval. |
| Queue Length | Vehicles queued at the intersection at the time of data collection. |
| Signal Phase Duration | Duration of traffic signal phases (green, yellow, red) in seconds. |
| Traffic Flow Rate | The rate of vehicles entering the intersection per minute. |
| Incident Data | Information on any incidents (e.g., accidents) reported at the intersection. |
| Weather Conditions | Description of the weather during data collection (e.g., sunny, rainy, foggy). |
| Day of the Week | Day of the week corresponding to the timestamp, affecting traffic patterns. |
| Traffic Type | Type of traffic observed (e.g., passenger cars, buses, trucks). |
| Geographic Coordinates | Latitude and longitude of the intersection location for mapping purposes. |

## *B. Optimization Algorithms*

The proposed system is dependent on two optimization algorithms: Artificial Bee Colony and Particle Swarm Optimization. Each algorithm is indispensable for optimizing traffic flow and overseeing signal timings. Particle Swarm Optimization is an ideal solution for optimizing traffic flow due to its exceptional performance in the face of continuous optimization challenges. The PSO algorithm is capable of functioning by representing potential traffic configurations as particles within a search region that has been previously established. The swarm's collective experiences and the individual experiences of each particle are used to refine the particle's location. The PSO's target function is mathematically expressed as follows to decrease the sum of the time that vehicles spend queuing at crossings:

$$
f(x) = \sum_{i=1}^{N} W_i \cdot T_i \tag{1}
$$

Where $f(x)$ is the objective function representing the total waiting time, N is the number of vehicles, $W_i$ is the waiting time for vehicle $i$, and $T_i$ is the time spent by the vehicle at the intersection. The update equation for the particle's velocity, which drives the optimization process, is given by:

$$
v_i^{t+1} = w \cdot v_i^t + c_1 \cdot r_1 \cdot (p_i^{best} - x_i^t) + c_2 \cdot r_2 (g^{best} - x_i^t) \tag{2}
$$
$$
x_i^{t+1} = x_i^t + v_i^{t+1} \tag{3}
$$

The position $x^t_i$ and velocity $v^t_i$ of the $i$-th particle are displayed below at iteration $t$. $w$ represents the inertia weight, $c_1$ and $c_2$ represent the cognitive learning element and social learning factor, respectively. Both $r_1$ and $r_2$ are variables that have a range of potential values. Global best position of the swarm is denoted by $g^{best}$, whereas the personal best position of the $i$-th particle is denoted by $p^{best}_i$. The location $x$ shows a set of signal timings for each intersection, which includes the duration of the green, yellow, and red lights. PSO iteratively searches for the optimal set of signal timings that minimizes traffic congestion. The objective function, $f(x)$, is defined as the total vehicle waiting time across all intersections:

$$
f(x) = \sum_{k=1}^{N} \sum_{j=1}^{T} W_{kj} \tag{4}
$$

The waiting time for vehicles at intersection $k$ during time step $j$ is denoted by $W_{kj}$, while $N$ denotes the no. of crossings in the network. The objective is to determine the optimal timing for the intersection's lighting in order to decrease $f(x)$. PSO is an ideal choice for the optimization of large-scale traffic networks due to its ability to facilitate global exploration and circumvent local optima. The Artificial Bee Colony algorithm is employed to enhance route planning by simulating the behavior of bees. The ABC model is analogous to a beehive, with each bee representing a prospective arrangement of the optimal route that minimizes fuel consumption and travel time. The fitness function guiding the ABC algorithm can be defined as:

$$
F = \alpha \cdot \text{Travel Time} + \beta \cdot \text{Fuel Consumption} \tag{5}
$$

Where $F$ is the overall fitness score, $\alpha$ and $\beta$ are weights that balance the importance of travel time and fuel consumption in the optimization process. Bees employ their fitness scores as a compass when optimizing their search for food sources or suitable routes. The algorithm directs the pollinators to forsake a suboptimal food source in order to locate a more suitable one. The flowchart diagram of the system that is proposed is shown in figure 1. The efficient exploration of the solution space by this group action ultimately determines the optimal routing options that

![This flowchart illustrates a traffic analysis system. It depicts a sequential process: data collection and cleaning lead to preprocessing. The preprocessed data feeds into traffic analysis, which uses transformers and PSO-ABC (likely an optimization algorithm). The analysis informs decision-making, followed by signal optimization with feedback to the traffic analysis stage. The flowchart's purpose is to visually represent the system's architecture and workflow.](_page_2_Figure_14.jpeg)

Figure 1. Flow Diagram of the ML and PSO-ABC System

alleviate traffic congestion. ABC is more exploratory and delays the appearance of less-than-ideal alternatives, whereas PSO and ABC can quickly determine the best course of action when they collaborate.

## *C. Machine Learning*

To improve the accuracy of traffic prediction, the system approach integrates Transformer networks into its machine learning component. The Transformer is an optimal choice for traffic pattern prediction due to its ability to keep long range of knowledge in sequential data. The model's heavy reliance on self-attention approaches enables it to quickly identify significant time periods and traffic features. The output of this mechanism is a weighted sum of the input values. It is determined by the degree of similarity between the inputs. The formula for self-attention is as follows:

$$
Attention(Q, K, V) = softmax(\frac{QK^{T}}{\sqrt{d_k}})V \tag{6}
$$

The matrices $Q$, $K$ and $V$ represent the query, key, and value, respectively, in this equation. The key vector's dimensionality is denoted as $d_k$. The gradients are stabilized through training by dividing the dot products by $\sqrt{d_k}$. In order to effectively manage the input sequence, transformers implement numerous layers of self-attention. In order to facilitate the model's prioritization of the input sequence for future traffic volume predictions, each layer generates a collection of attention scores. The model can predict the behavior of traffic in a different circumstance, including normal flows and unusual occurrences such as accidents or road obstructions, as a result of its focus on learning patterns over time. It is essential to preserve the sequence order for time-series data, such as traffic flow, and positional encodings can further enhance the model's performance. Positional encoding can be expressed as follows:

$$
PE_{(pos, 2i)} = \sin \left( \frac{pos}{10000^{\frac{2i}{d_{model}}}} \right) \tag{7}
$$

$$
PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{\frac{2i}{d_{model}}}}\right) \tag{8}
$$

The dimensionality of the model is denoted by the symbol $d_{model}$ while the position in the sequence is represented by the symbol $pos$. These encodings enable the Transformer model to preserve the sequence order, which is a critical characteristic for precise prediction. The historical traffic data that is employed to train the model encompasses variables such as vehicle counts, velocities, and weather conditions. The Transformer model's predictive capabilities can be improved by incorporating a variety of data points. Two examples of sophisticated loss functions that can be continuously adjusted in response to real-time data inputs and provide accurate predictions are Mean Squared Error and Mean Absolute Error. The proposed hybrid optimization and machine learning framework accomplishes optimal performance by integrating the strengths of Transformer networks with those of PSO and ABC algorithms. This integrated approach optimizes urban traffic management by reducing vehicle delay times and improving route planning, thereby improving the accuracy of traffic forecasts. Figure 2 depicts the architecture of the transformers. The proposed paradigm establishes the foundation for more sustainable and intelligent cities by improving urban transportation solutions through real-time responsiveness and flexibility in response to evolving traffic conditions.

![The image is a block diagram illustrating a sequence-to-sequence model architecture using a transformer network. It shows an encoder and a decoder, each composed of multiple transformer layers. Input feeds into the encoder, which processes it and passes the result to the decoder. The decoder generates the output. The diagram visually depicts the data flow and layered structure of this neural network architecture.](_page_3_Figure_8.jpeg)

Figure 2. Transformers Model

## IV. RESULT AND DISCUSSION

The effectiveness of the proposed urban traffic management approach was assessed using a real-world dataset, which incorporates optimization and machine learning. The primary objectives of the study were to enhance the reliability of traffic predictions, manage traffic flow, and decrease vehicle delay times. A comprehensive comprehension of the model's performance is facilitated by visual representations, qualitative annotations, and numerical data. Various metrics, including the average voyage duration, average vehicle waiting time, and overall fuel consumption, were assessed to evaluate the model. Comparisons were made between the measures and the baseline findings of the conventional traffic management system. The proposed model was assessed in comparison to more conventional methodologies, as illustrated in Table 1.

TABLE I. PERFORMANCE METRICS COMPARISON

| Metric | Traditional Method | Proposed Model |
|---|---|---|
| Average Vehicle Waiting Time (s) | 120 | 75 |
| Average Travel Time (s) | 300 | 225 |
| Fuel Consumption (L) | 50 | 35 |

The proposed method reduces fuel consumption by 30%, average travel time by 25%, and average vehicle waiting time by 37.5%. The plan was successful in reducing overall travel costs and enhancing traffic flow, as evidenced by these results. The model was deployed to a specific urban area, and real-time traffic conditions were monitored to derive qualitative findings. The PSO and ABC algorithms can be integrated to modify traffic signal timings in real-time based on data, showing a efficient and rapid traffic flow. By employing its self-attention mechanism, the Transformer model was capable of predicting potential congestion scenarios, identifying peak traffic hours, and implementing preventative measures to mitigate traffic delays. As an outcome of the proposed model's capacity to simulate a variety of traffic scenarios, traffic management authorities reported enhanced decision-making strategies. The CPDT architecture enabled operators to make informed modifications in real-time by graphically displaying traffic conditions. Figure 3 illustrates the actual traffic in each 1-hour time period with the predicted values. The model is able to predict better with less error.

![The bar chart compares actual and predicted traffic volume at hourly intervals. Blue bars represent actual traffic counts, while orange bars show predicted values. The chart aims to demonstrate the accuracy of a traffic volume prediction model by visually comparing the predicted traffic volume with the actual traffic volume observed over different time periods.](_page_4_Figure_0.jpeg)

Figure 3. Actual vs Predicted Traffic Volume

The relationship between traffic volumes and congestion levels was also examined both prior to and following the model's implementation. The traffic volume and congestion levels are summarized in Table 2.

TABLE II. TRAFFIC VOLUME AND CONGESTION LEVELS

| Time Period | Traffic Volume (vehicles/hour) | Congestion Level | Proposed Model Congestion Level |
|---|---|---|---|
| Morning Peak | 1500 | 8 | 4 |
| Afternoon Peak | 1800 | 9 | 5 |
| Evening Peak | 1600 | 7 | 3 |

Table 2 illustrates that congestion levels experienced substantial reductions during a variety of prime hours. The proposed methodology demonstrated its capacity to effectively manage high traffic volumes by reducing congestion from 8 to 4 in the morning peak, a significant accomplishment. An analysis was conducted to determine the accuracy of traffic forecasting by comparing the expected and actual traffic levels. Table 3 contains a summary of the Transformer model's predictions' accuracy.

TABLE III. PREDICTIVE ACCURACY OF TRAFFIC FORECASTING

| Time Interval | Actual Traffic Volume (vehicles) | Predicted Traffic Volume (vehicles) | Mean Absolute Error (MAE) (vehicles) | Mean Absolute Percentage Error (MAPE) (%) |
|---|---|---|---|---|
| 8 AM - 9 AM | 500 | 480 | 20 | 4.00 |
| 9 AM - 10 AM | 550 | 530 | 20 | 3.64 |
| 10 AM - 11 AM | 600 | 590 | 10 | 1.67 |
| 11 AM - 12 PM | 650 | 640 | 10 | 1.54 |
| 12 PM - 1 PM | 600 | 590 | 10 | 1.67 |
| 1 PM - 2 PM | 700 | 680 | 20 | 2.86 |
| 2 PM - 3 PM | 750 | 740 | 10 | 1.33 |
| 3 PM - 4 PM | 800 | 790 | 10 | 1.25 |
| 4 PM - 5 PM | 900 | 880 | 20 | 2.22 |
| 5 PM - 6 PM | 800 | 780 | 20 | 2.50 |
| 6 PM - 7 PM | 600 | 610 | 10 | 1.67 |

The model's exceptional ability to forecast future traffic levels is evidenced by its consistently low Mean Absolute Error (MAE). The model's predictions are verified by the Mean Absolute Percentage Error (MAPE) percentages, which are less than 5% for each period. Table 4 compares the proposed hybrid model with other traffic prediction models, showcasing its superior prediction accuracy, lower mean absolute error (MAE), and faster computational time for real-time traffic management.

TABLE IV. COMPARISON WITH OTHER MODELS

| Optimization Algorithm(s) | ML Model | MAE (vehicles) | MAPE (%) | Prediction Accuracy (%) | Computational Time (ms) |
|---|---|---|---|---|---|
| PSO & ABC | Transformer Networks | 15 | 2.18 | 97.82 | 450 |
| Genetic Algorithm (GA) | LSTM | 30 | 5.12 | 94.88 | 700 |
| Ant Colony Optimization (ACO) | RNN | 28 | 4.85 | 95.15 | 670 |
| Simulated Annealing (SA) | GRU | 22 | 3.66 | 96.34 | 600 |
| Particle Swarm Optimization | LSTM | 25 | 4.12 | 95.88 | 580 |
| Artificial ABC | CNN-LSTM Hybrid | 20 | 3.25 | 96.75 | 500 |

## V. CONCLUSION

The proposed urban traffic control system has been demonstrated to be extremely efficient and accurate by integrating machine learning and optimization. The Cyber-Physical Digital Twin (CPDT) design was improved by the integration of real-time data, which improved signal timings and traffic flow. The combination of Artificial Bee Colony and Particle Swarm Optimization algorithms resulted in a 15% reduction in vehicle delay times and a 12% improvement in route planning. The Transformer model achieved an accuracy of 93% in traffic predictions, with a mean absolute error (MAE) of 0.14. The system is effective in managing traffic in urban areas, which reduces congestion and increases productivity, according to the findings. Future research is on enhancing the CPDT design's scalability and enhancing the model's adaptability to unforeseen traffic events, such as sudden incidents or road construction, in order to more effectively manage traffic in larger urban areas.

### REFERENCES

- <a id="ref-1"></a>[[1]](#ref-1) Kumar, M., Kumar, K. and Das, P., 2021. Study on road traffic congestion: A review. Recent Trends in Communication and Electronics, pp.230-240.
- <a id="ref-2"></a>[[2]](#ref-2) Samal, S.R., Mohanty, M. and Santhakumar, S.M., 2021. Adverse effect of congestion on economy, health and environment under mixed traffic scenario. Transportation in Developing Economies, 7(2), p.15.
- <a id="ref-3"></a>[[3]](#ref-3) Lu, J., Li, B., Li, H. and Al-Barakani, A., 2021. Expansion of city scale, traffic modes, traffic congestion, and air pollution. Cities, 108, p.102974.
- <a id="ref-4"></a>[[4]](#ref-4) Santhosh, K.K., Dogra, D.P. and Roy, P.P., 2020. Anomaly detection in road traffic using visual surveillance: A survey. ACM Computing Surveys (CSUR), 53(6), pp.1-26.
- <a id="ref-5"></a>[[5]](#ref-5) Valença, G., Moura, F. and de Sá, A.M., 2021. Main challenges and opportunities to dynamic road space allocation: From static to dynamic urban designs. Journal of urban mobility, 1, p.100008.
- <a id="ref-6"></a>[[6]](#ref-6) Hamdi, M.M., Audah, L., Rashid, S.A. and Al Shareeda, M., 2020. Techniques of Early Incident Detection and Traffic Monitoring Centre in VANETs: A Review. J. Commun., 15(12), pp.896-904.
- <a id="ref-7"></a>[[7]](#ref-7) J. Zhang, Z. Zhang and X. Lin, "An Improved Artificial Bee Colony with Self-Adaptive Strategies and Application," 2021 International Conference on Computer Network, Electronic and Automation (ICCNEA), Xi'an, China, 2021, pp. 101-104, doi: 10.1109/ICCNEA53019.2021.00032.
- <a id="ref-8"></a>[[8]](#ref-8) T. M. Shami, A. A. El-Saleh, M. Alswaitti, Q. Al-Tashi, M. A. Summakieh and S. Mirjalili, "Particle Swarm Optimization: A Comprehensive Survey," in IEEE Access, vol. 10, pp. 10031-10061, 2022, doi: 10.1109/ACCESS.2022.3142859.
- <a id="ref-9"></a>[[9]](#ref-9) M. C et al., "Intelligent Traffic Monitoring, Prioritizing and Controlling Model based on GPS," 2023 International Conference on Innovative Data Communication Technologies and Application (ICIDCA), Uttarakhand, India, 2023, pp. 297-299, doi: 10.1109/ICIDCA56705.2023.10100296.
- <a id="ref-10"></a>[[10]](#ref-10) N. Gupta, S. Saawan, S. Kumar and M. U. Khan, "Enhancing Traffic Flow Efficiency and Mitigating Congestion through ML-Based Traffic Management Strategies," 2023 International Conference on Advances in Computation, Communication and Information Technology (ICAICCIT), Faridabad, India, 2023, pp. 737-743, doi: 10.1109/ICAICCIT60255.2023.10466042.
- <a id="ref-11"></a>[[11]](#ref-11) B. R. Kumar, N. K. Chikkakrishna and T. Tallam, "Short Term Predictions of Traffic Flow Characteristics using ML Techniques," 2020 4th International Conference on Electronics, Communication and Aerospace Technology (ICECA), Coimbatore, India, 2020, pp. 1504- 1508, doi: 10.1109/ICECA49313.2020.9297552.
- <a id="ref-12"></a>[[12]](#ref-12) G. B. Madhavi, A. D. Bhavani, Y. S. Reddy, A. Kiran, N. T. Chitra and P. C. S. Reddy, "Traffic Congestion Detection from Surveillance Videos using Deep Learning," 2023 International Conference on Computer, Electronics & Electrical Engineering & their Applications (IC2E3), Srinagar Garhwal, India, 2023, pp. 1-5, doi: 10.1109/IC2E357697.2023.10262545.
- <a id="ref-13"></a>[[13]](#ref-13) M. S. Raza, K. Aziz Bhatti, F. M. Malik and S. Amin Sheikh, "Network Traffic Classification using Deep Neural Networks," 2023 International Conference on Frontiers of Information Technology (FIT), Islamabad, Pakistan, 2023, pp. 85-89, doi: 10.1109/FIT60620.2023.00025.
- <a id="ref-14"></a>[[14]](#ref-14) V. D. Chaudhari, A. J. Patil, D. J. Shirale, T. R. Al-Shaikhli, A. V. Kumar and B. Eswaran, "Improving Traffic Flow in Smart Cities with Machine Learning-Based Traffic Management," 2024 Ninth International Conference on Science Technology Engineering and Mathematics (ICONSTEM), Chennai, India, 2024, pp. 1-5, doi: 10.1109/ICONSTEM60960.2024.10568728.
- <a id="ref-15"></a>[[15]](#ref-15) S. Godhbani, S. Elkosantini, S. M. Lee and W. Suh, "A New Multimodal and Spatio-Temporal Dataset for Traffic Control: Development, Analysis, and Potential Applications," 2024 IEEE International Conference on Advanced Systems and Emergent Technologies (IC_ASET), Hammamet, Tunisia, 2024, pp. 1-5, doi: 10.1109/IC_ASET61847.2024.10596210.
- <a id="ref-16"></a>[[16]](#ref-16) S. C, S. Radhika, M. K, S. Ranjith and N. Sasirekha, "An intelligent IoT Enabled Traffic queue handling System Using Machine Learning Algorithm," 2022 International Conference on Innovative Computing, Intelligent Communication and Smart Electrical Systems (ICSES), Chennai, India, 2022, pp. 1-9, doi: 10.1109/ICSES55317.2022.9914294.
- <a id="ref-17"></a>[[17]](#ref-17) P. K. Barik, K. Munjpara, A. Gevariya, H. Mangukiya, M. Kotadiya and N. Mulani, "Density-Based Automatic Traffic Control Using Machine Learning," 2023 IEEE 11th Region 10 Humanitarian Technology Conference (R10-HTC), Rajkot, India, 2023, pp. 97-102, doi: 10.1109/R10-HTC57504.2023.10461753.
- <a id="ref-18"></a>[[18]](#ref-18) M. Pagale, R. Purohit, P. Dhade, A. Thakare, S. Gudadhe and P. Narkhede, "Insights of Deep Convolutional Neural Network for Traffic Sign Detection in Autonomous Vehicle," 2023 2nd International Conference on Applied Artificial Intelligence and Computing (ICAAIC), Salem, India, 2023, pp. 176-181, doi: 10.1109/ICAAIC56838.2023.10141095.

## Metadata Summary
### Research Context
- **Research Question**: How can advanced technologies improve urban traffic management and reduce congestion?
- **Methodology**: CPDT architecture, hybrid PSO-ABC optimization, Transformer networks for prediction, multi-source data integration
- **Key Findings**: 20% reduction in average traffic delays, 15% increase in prediction accuracy, demonstrated effective hybrid optimization approach
- **Primary Outcomes**:

### Analysis
- **Limitations**: Limited to traffic management domain, computational complexity not discussed
- **Research Gaps**:
- **Future Work**: Apply to personal schedule optimization, integrate with HDM planning systems, develop user-friendly interfaces
- **Conclusion**: Shows promise for intelligent system optimization using advanced computational techniques

### Implementation Notes
Agent Epsilon: Hybrid optimization techniques applicable to HDM predictive modeling and resource optimization