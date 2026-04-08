# SplaTraj: Camera Trajectory Generation with Semantic Gaussian Splatting

Xinyi Liu<sup>1,2</sup>, Tianyi Zhang<sup>1</sup>, Matthew Johnson-Roberson<sup>1</sup> and Weiming Zhi<sup>1</sup>

Abstract—Many recent developments for robots to represent environments have focused on photorealistic reconstructions. This paper particularly focuses on generating sequences of images from the photorealistic Gaussian Splatting models, that match instructions that are given by user-inputted language. We contribute a novel framework, SplaTraj, which formulates the generation of images within photorealistic environment representations as a continuous-time trajectory optimization problem. Costs are designed so that a camera following the trajectory poses will smoothly traverse through the environment and render the specified spatial information in a photogenic manner. This is achieved by querying a photorealistic representation with language embedding to isolate regions that correspond to the user-specified inputs. These regions are then projected to the camera's view as it moves over time and a cost is constructed. We can then apply gradient-based optimization and differentiate through the rendering to optimize the trajectory for the defined cost. The resulting trajectory moves to photogenically view each of the specified objects. We empirically evaluate our approach on a suite of environments and instructions, and demonstrate the quality of generated image sequences.

## I. INTRODUCTION

Autonomous agents operating in unknown environments need to construct internal representations of their operating environment. Traditionally, these representations, such as occupancy or semantic maps, can be difficult for the untrained eye to interpret. Recent advances in computer vision have led to the development of *photorealistic* 3D environment representations [1], which enable high-fidelity visualizations of the robot's surroundings. Of these representations, Gaussian Splatting models [2] have emerged as the model of choice due to their ability to render photorealistic images efficiently. There is great excitement within the community to advance methodologies for constructing Gaussian Splatting models [3] and embedding additional properties into them. Yet many unsolved challenges exist around how best to leverage these representations for downstream tasks.

A valuable downstream task for Gaussian Splatting is to take advantage of its visual realism to extract visually accurate sequences of images. This paper tackles this challenge. Specifically, we study the problem of generating a sequence of photorealistic images from a Gaussian Splatting model that smoothly displays a sequence of objects that human users can semantically specify. In particular, we introduce the SplaTraj framework, which formulates a

<span id="page-0-0"></span>![](_page_0_Figure_9.jpeg)

Fig. 1: We propose SplaTraj, which enables users to provide semantic instructions consisting of a sequence of objects. This is then formulated as a gradient-based trajectory optimization problem within a photorealistic Gaussian Splatting model, whose solution smoothly shows us each of the objects.

trajectory optimization problem that attempts to optimally position the camera, such that it smoothly moves through the reconstructed environment while accurately pointing, in order, to each of the semantically specified objects within the scene.

SplaTraj operates on top of Gaussian Splatting models that encode visual language features into the environment reconstruction. Then, embedded semantics in the environment are compared with user-inputted language semantics to identify objects and regions within the environment that are relevant to the user's intended instruction. These identified objects are rendered into the view of the camera and carefully designed costs evaluate the quality of their visual placement. SplaTraj parameterized camera trajectories as continuous time-varying functions. By applying gradient-based optimizers to the costoptimal motion trajectory, we can differentiate through both the rendering equation and the trajectory parameterization. This enables us to obtain a model that describes the optimal camera motion through the environment so that we can photogenically capture all of the objects specified by the user. A simple overview is illustrated in fig. 1.

Concretely, our technical contributions are:

- The SplaTraj framework, which formulates generating image sequences as a continuous trajectory optimization problem over camera poses;
- Methodology to extract environment structure from user-inputted semantics and then incorporate the structures as an optimization cost for trajectory optimization;
- Empirical evaluation of SplaTraj to generate images in a variety of benchmark Gaussian Splatting environments.

<sup>&</sup>lt;sup>1</sup> Robotics Institute, Carnegie Mellon University, Pittsburgh, PA, USA Email: wzhi@andrew.cmu.edu

<sup>&</sup>lt;sup>2</sup> Joint Department of Biomedical Engineering, University of North Carolina-Chapel Hill, Raleigh, NC, USA Email: xinyili@ad.unc.edu

## II. RELATED WORK

Robot Representations and Photorealistic Representations: Robots operating in unknown environments rely on constructing internal representations of the environment. These have generally been representations of occupancy [4], [5], [6], surfaces [7], or motion patterns [8], [9]. However, such representations are often difficult for the untrained eye to interpret. This has led to photorealistic representations, such as Neural Radiance Fields (NeRFs) [1], and more 3D Gaussian Splatting [2]. Subsequent works [10], [3], [11] in this area augment the capabilities of photorealistic reconstructions. Our work leverages efforts in embedding language features [12] into realistic representations [13].

Camera Optimization: Our work is tangentially related to camera placement optimization, which has been an active area of research. [14] propose an automatic camera placement method for generating image-based models from scenes with known geometry. Albahri et. al [15] explore camera placement within buildings, focusing on maximizing. Another work in this space, [16] addresses the optimal placement of cameras for human activity recognition, maximizing the observability. Our work differs from this body of work in that our optimization occurs within a photorealistic reconstruction and is driven by user-provided semantics.

**Trajectory Optimization:** Trajectory optimization is commonly used within motion planning [17], [18], [19] and control to obtain motion sequences to reach a certain goal. Prominent trajectory optimization methods within motion planning, including TrajOpt [20], CHOMP [21], STOMP [22]. Trajectory optimization for a finite horizon also appears within model predictive control [23]. Prominent trajectory optimization methods include MPPI [24]. Recent approaches have also been introduced [25], [26], [27], [28] to generate motions reactively. This shortens the time horizon even further. Classic trajectory optimization formulates an objective that finds a minimal distance path. Our work differs from these approaches in that we formulate a cost within trajectory optimization that optimizes object placement within the camera view, by differentiating the camera rendering.

#### III. PRELIMINARIES

## A. Open Querying on Images

Open query refers to the ability of the model to handle arbitrary text inputs for image retrieval or classification tasks, without being limited to a predefined set of categories or labels. Contrastive Language-Image Pre-Training [29] is commonly used for tasks of this class. CLIP jointly trains an image encoder and a text encoder to predict the correct pairings of a batch of training examples. CLIP is typically used as a plug-and-play encoder. It is trained on a large-scale dataset of 400 million image-text pairs, enabling it to learn visual concepts from natural language descriptions. In this paper, we also use the pre-trained encoder provided in CLIP to generate embeddings from semantic inputs.

## B. Gaussian Splatting and Language Field

Gaussian Splatting[2] explicitly represents a 3D scene as a collection of anisotropic 3D Gaussians, with each Gaussian G(x) characterized by a mean  $\mu \in \mathcal{R}^3$  and a co-variance matrix  $\Sigma$ :

$$G(x) = \exp\left(-\frac{1}{2}(x-\mu)^{\top}\Sigma^{-1}(x-\mu)\right)$$

For each camera pose in the image sequence, an image can be synthesized from the following rendering equation [2]:

$$\hat{I} = \sum_{i \in \mathcal{N}} c^i \alpha^i \prod_{j=1}^{i-1} (1 - \alpha^j)$$
 (1)

where  $c^i$  is the color of the *i*-th Gaussian,  $\mathcal{N}$  denotes the Gaussians in the tile, and  $\alpha^i = o^i G_{2D}^i(v)$ . Here  $o^i$  is the opacity of the *i* th Gaussian and  $G_{2D}^i(\cdot)$  represents the function of the *i*-th Gaussian projected onto 2D. Recent research has enhanced 3D Gaussians with language features [30][13].

$$\hat{I}_{l} = \sum_{i \in \mathcal{N}} l^{i} \alpha^{i} \prod_{j=1}^{i-1} \left(1 - \alpha^{j}\right)$$

where  $l^i$  is the open-vocabulary feature embedding of i-th 3D gaussian primitives and  $\hat{I}_l$  represents the rendered open-vocabulary feature embedding at pixel u. The intuition here is simple: positions in the scene are mapped to language features rather than colors. We use upper script index notation specifically for the 3D Gaussian index, to distinguish it from other index notations in the paper.

## IV. METHODOLOGY

<span id="page-1-0"></span>In this section, we proposed our differentiable optimization method to solve photogenic trajectory generation of the openqueried objects represented in 3D Gaussians. The overall framework is shown in Fig. 2.

#### A. Problem Formulation

This paper addresses the optimization problem of generating realistic camera trajectories in environments represented by language-annotated 3D Gaussians [13]. Given a user-specified query of various modalities such as text,  $Q = (q_1, q_2, \ldots, q_n)$ , our goal is to determine a trajectory of camera pose  $\Phi \in SE(3)$  over a normalized period  $t \in [0, 1]$ .

The camera poses should sequentially focus on the objects corresponding to each  $w_i$  within the specific time intervals  $T_i = \left[\frac{i-1}{n}, \frac{i}{n}\right] \left(\bigcup_i T_i = 1, \bigcap_i T_i = \emptyset\right)$ . Our objective is to render photogenic videos during these intervals.

In this context, a photo is considered more photogenic if the specified object is more centered in the image and occupies a portion closer to a user-defined ratio. Formally, we seek to optimize the camera trajectory such that each object  $w_i$  is appropriately captured in its designated time slot, resulting in a series of well-composed images.

The challenge lies in dynamically adjusting the camera trajectory to meet these criteria while smoothly transitioning between different objects in the sequence.

<span id="page-2-0"></span>![](_page_2_Figure_0.jpeg)

Fig. 2: Pipeline overview: Our method consists of two main steps, vocabulary querying and gradient-based trajectory optimization. We generate a 3D object mask based on language embeddings and trained language fields in the vocabulary query step. In trajectory optimization, we use the differential renderer to generate rendering-based cost and gradient descent to update the trajectory coefficients. The 3D confidence heatmap derived in preprocessing is fixed in the downstream differential rasterization.

#### B. Semantic Map Extraction

We seek to ground semantic specifications given by the user to physical coordinates within our splatting model. We leverage the semantic information encoded in the 3D Gaussians to generate a differentiable object mask for each word query, following a similar procedure in [31].

The relevancy score on a Gaussian  $G^j$  is defined as a softmax score on the

$$S(G^{j}) = \min_{i} \frac{\exp(\varpi_{G}^{j} \cdot \varpi_{qry})}{\exp(\varpi_{G}^{j} \cdot \varpi_{qry}) + \exp(\varpi_{G}^{j} \cdot \varpi_{canon}^{i})}, \quad (2)$$
 where  $\varpi_{canon}^{i}$  is the CLIP embeddings of a predefined

where  $\varpi_{canon}^i$  is the CLIP embeddings of a predefined canonical phrase chosen from "object", "things", "stuff", and "texture". Experimentally, we found that a DBScan algorithm [32] on top relevancy score percentile Gaussians can filter out irrelevant noises in 3D space. The relevancy score suffered from the score scale ambiguity and spread outliers in 3D space, which would cause unclear mask edges and outliers in the rendering result, leading to downstream failure. A binary channel for object prompt  $q_i$  based on the original 3D Gaussian field is attained in the filtering procedure, where the  $j^{\text{th}}$  entry of the  $q_i$  binary channel is  $b_i^j = \mathbb{I}_{G^j \in \mathcal{N}_i}$ , where  $\mathbb{I}_{\{A\}}$  is the indicator of event A,  $\mathcal{N}_i$  is the set of Gaussians after filtering of prompt  $q_i$ .

We rendered 2D binary mask via the following rendering equation:

<span id="page-2-1"></span>
$$I_b = \sum_{i \in \mathcal{N}} b^i \alpha^i \prod_{j=1}^{i-1} \left( 1 - \alpha^j \right). \tag{3}$$

By rendering the mask onto the camera view, we can reason about properties in the camera's view. This includes the ratio of the object within the frame, giving an indication of how photogenic the rendered image is.

#### C. Continuous Trajectory Representation

Many trajectory optimization problems express trajectories as a sequence of waypoints. This typically requires *a priori* discretization of the trajectory at some fixed time resolution. Here, we take an alternative approach and represent the motion trajectory of the camera as a continuous function, mapping from a normalized time parameter to the camera

pose. This enables us to generate trajectories of any desired resolution.

To represent a camera trajectory vector function in 6 dimensions, we use 6 independent functions to model each variable of

$$\mathbf{\Phi}(t) = [r_x(t), r_y(t), r_z(t), x(t), y(t), z(t)]^{\top}, \qquad (4)$$

where  $r_x, r_y, r_z$  are rotation vectors of transformation from the world coordinate to the camera coordinate, x, y, z are translation components of  $t \in [0,1]$ . We represent this function concisely as a combination of Squared Exponential Radial Basis Functions (RBFs). Specifically, the j-th entry of  $\Phi(t)$  could be represented by a weighted sum of RBFs:

$$[\mathbf{\Phi}(t)]_j = \sum_{i=1}^N w_i^j \psi_i(t) = \mathbf{w}_j^\top \mathbf{\Psi}(t), \tag{5}$$

where  $\mathbf{w}_j = (w_1^j, w_2^j, ..., w_N^j)$  is the weight vector associated with the j-th entry, and  $\mathbf{\Psi}(\mathbf{t}) = (\psi_1(t), \psi_2(t), ..., \psi_N(t))$  is the packed RBFs, assigned with entry-specific weight vector  $\mathbf{w}_i$ . We use the Gaussian function as our basis function as

$$\psi_i(t) = \exp\left(-\left(\frac{(t-t_i)^2}{2\sigma^2}\right)\right),$$
 (6)

where  $t_i = \frac{i}{n} - \frac{1}{2}$ , i = 1, 2, ..., n is the center of the time interval  $T_i$ , hyper-parameter  $\sigma$  is the standard deviation of the Gaussian distribution. This representation offers a smooth and flexible trajectory generation by interpolating between control points with a smooth basis function. Notably, our trajectory formulation enables us to query and obtain a camera pose at arbitrary time and at arbitrary time resolution.

## D. Cost Function

We constructed an optimization problem to generate trajectories that minimize the defined cost so that the camera can sequentially fixate on objects corresponding to language inputs given by the user  $Q=(q_1,q_2,\ldots,q_n)$ , we are optimizing the following cost function, defined as a piecewise function distributing each object prompt to the time interval  $T_i=\left\lceil\frac{i-1}{n},\frac{i}{n}\right\rceil$ , specifically,

$$\arg\min_{\mathbf{w}} \quad \sum_{i=1}^{n} \int_{T_i} L^{q_i}(\mathbf{\Phi}_{\mathbf{w}}(t)) dt, \tag{7}$$

where  $L^{q_i}(\cdot)$  is the cost for prompt word query  $q_i$ . To obtain the cost, we shall render the identified semantically-relevant

3D structure to the camera's view to obtain a binary mask. We denote the mask as  $I_b$  and compute by evaluating eq. (3). We define  $L^{q_i}$  as the sum of multiple cost terms,

$$L^{q_i} = L_{TCE} + L_{TRE} + L_{upright} + \alpha L_{prior}$$
. (8) Here,  $\alpha$  is a weight of the cost term  $L_{prior}$  which gradually decays. The definitions of each cost term are elaborated below.

The rendering-based cost includes the center cost and the ratio cost. Here we render of object that we identify as relevant to the user's prompt as a binary mask, denoted  $I_b$ and computed by evaluating eq. (3). Then  $L^{q_i}$  is the sum of the following terms:

1) Target Centralizing Error (TCE) Cost:

$$L_{TCE}(I_b) = ||(\frac{c_x}{H}, \frac{c_y}{W}) - (\frac{1}{2}, \frac{1}{2})||_2,$$
 where  $(c_x, c_y) = center(I_b)$  are pixel coordinates of the

center of the mask.

2) Target Ratio Error (TRE) Cost:

$$L_{TRE}(I_b) = ||\frac{sum(I_b)}{HW} - r_t||_2,$$
 (10)

where  $sum(I_b)$  counts the area of the 2D binary mask  $I_b$ .

3) Uprightness Cost: The camera's orientation can be regulated to an upright position by the following cost term

$$L_{upright} = -\langle \mathbf{e_z}, \mathbf{Re_x} \rangle, \tag{11}$$

Where we use the inner product between the world unit upward direction axis  $e_z$  and the camera's unit upright axis  $Re_x$  where e are unit coordinate vector and R denotes the rotation from camera frame to world frame.

4) Diminishing Prior Cost: We warm-start the optimization via a prior cost which guides the camera toward the physical adjacency of the target objects. This is given:

$$L_{prior} = -\max(r, \|\mathbf{c} - \mathbf{o}\|_2) - \frac{(\mathbf{c} - \mathbf{o})_z^C}{\|\mathbf{c} - \mathbf{o}\|_2}.$$
 (12)

The first term in the  $L_{prior}$  calculates a cost based on the proximity of the camera to the object, with a minimum distance threshold defined by the radius; The second term of the  $L_{prior}$  calculates the angle deviation from the object, specifically measured by the inner product between camera direction unit vector with the normalized vector pointing from object to the camera center.

During optimization, we utilize the differential renderer to calculate the rendering-based cost  $L_{TCE}$ ,  $L_{TRE}$  and  $L_{IoU}$ , whose gradient with respect to trajectory coefficient  $\frac{\partial L}{\partial \mathbf{w}}$  can be attained from the differential renderer. We warm-start the progress by giving an exponentially decaying coefficient to differentiable prior term  $L_{prior}$ . The total cost gradient with respect to trajectory coefficient w would update the trajectory coefficient via Adam optimizer[33], iteratively refining the camera trajectory.

#### V. EMPIRICAL RESULTS

## A. Experiments Overview

In this section, we seek to investigate empirically:

• Whether the image cost design leads to object-centered, properly distanced, and occlusion-avoiding rendering images; (Section V-B)

<span id="page-3-1"></span>

|          | Scenarios | $\overline{TCE} \downarrow$ | $\overline{TRE}\downarrow$ | $\overline{IoU} \uparrow$ |
|----------|-----------|-----------------------------|----------------------------|---------------------------|
| 3D Prior | Teatime   | 0.066                       | 0.321                      | 0.531                     |
| SD FIIOI | Figurines | 0.051                       | 0.220                      | 0.522                     |
|          | Kitchen   | 0.151                       | 0.262                      | 0.527                     |
| TCE      | Teatime   | 0.014                       | 0.119                      | 0.805                     |
| ICE      | Figurines | 0.010                       | 0.117                      | 0.480                     |
|          | Kitchen   | 0.120                       | 0.112                      | 0.617                     |
| TRE      | Teatime   | 0.018                       | 0.068                      | 0.808                     |
| IKE      | Figurines | 0.115                       | 0.126                      | 0.384                     |
|          | Kitchen   | 0.021                       | 0.057                      | 0.711                     |
| TCE+TRE  | Teatime   | 0.029                       | 0.057                      | 0.867                     |
|          | Figurines | 0.081                       | 0.107                      | 0.760                     |
|          | Kitchen   | 0.098                       | 0.065                      | 0.751                     |

TABLE I: Result from single camera pose optimization with randomly selected queries, 10 repetitions with randomized initial decision variable.

- If the photogenic objective of the optimization would lead to new challenges and properties, such as multiple optimal solutions;
- Whether the trajectory representation used is amenable to optimization with respect to the objective defined.

We validate our method in both single-pose optimization settings in Section V-B and trajectory optimization settings in Section V-C.

## <span id="page-3-0"></span>B. Single Pose Optimization

To ensure that the pose-wise cost function components are correct, we first design a single pose optimization to validate our method. Instead of optimizing the trajectory weight coefficient, we optimize on individual poses, using the same cost function defined in section IV. The objective function is therefore reduced to  $\arg\min_{\mathbf{\Phi}} L^{q_i}(\mathbf{\Phi})$ , where  $\Phi = [r_x, r_y, r_z, x, y, z]$  is the optimization variable.

With each selected query prompt  $q_i$ , we preprocess the scene dataset by extracting the semantic mask. During optimization, we calculate the cost value and gradient of the current pose and run gradient descent on the cost manifold  $L^{q_i}$ . We use the ADAM optimizer to evaluate the optimization result's TCE, TRE, and IoU score after 400 iterations. We also did an ablation study to show the effect of each optimization cost term, as shown in table I. We first show theimpact of 3D prior terms, which includes all terms derived from 3D prior information without decaying weights; We then apply TCE and TRE regulating terms separately and jointly, with 3D prior terms with diminishing weight through steps. Our results show:

- TCE cost term applied in the optimization can centralize objects better, and enabling centering cost or ratio regulation cost might improve the performance of the corresponding aspect.
- The benefit of TCE and TRE can be additive, and combining the two regulating terms generally finds the best pose.
- The IoU alone does not significantly improve the overall performance. In the experiment, we observe the nonsmoothness of the IoU cost function, leading to huge steps in gradient descent that lead out of the low-cost region, similar issues have been discussed in the object detection field [34].

<span id="page-4-3"></span>![](_page_4_Figure_0.jpeg)

Fig. 3: Visualization of SplaTraj results across Scenarios: We selected 9 evenly spaced keyframes from the trajectory sequence for visualization. We present the rendered masks and rendered RGB images with overlaid blue masks. We observe that as the camera moves along the resulting trajectory, each of the semantically specified objects appear prominently in view.

<span id="page-4-1"></span>![](_page_4_Figure_2.jpeg)

Fig. 4: A batch of camera poses before and after SGLD process. In (a), the initialized camera poses at iteration 0. In (b), optimized poses after 200 iterations of SGLD, where the cameras are pointing towards the target object (in blue).

1) Stochastic Gradient Langevin Dynamics (SGLD) [35]: We generated 20 random poses and run SLGD to optimize the their poses. As shown in Fig. 4. Rather than converging to a single deterministic solution, SGLD enables a principled approximation of the posterior distribution of the optimized camera pose. This forms a ring-shaped array pointing to the object. The wide spread in camera posterior distribution reflects that the ring-shaped low-cost region has multiple local minima, leading to different optimization results using randomized initial conditions.

#### <span id="page-4-0"></span>C. Trajectory Optimization

We evaluate the qualities of trajectories obtained via SplaTraj. We compare our trajectory formulation against two other baseline trajectory representations. The experiment follows a similar procedure as the single pose experiment in V-B. In each experiment, we provide text prompt instruction queries to visit 3 objects within each scene. Renderings

<span id="page-4-2"></span>![](_page_4_Picture_7.jpeg)

Fig. 5: Gaussian Splatting rendering of queried objects

of these objects are illustrated in fig. 5. During each optimization, the ADAM [36] optimizer is run to minimize the cost manifold  $L^{q_i}$  for 200 iterations, the TCE, TRE, and IoU scores are then collected from the optimized trajectories using different trajectory representations.

**Baselines:** We evaluate the performance of SplaTraj against the other two commonly used representations: way-point basis and polynomial basis.

1) Waypoint Representation: The following expression defines the waypoint basis functions:

$$\psi_i(t) = \mathbb{I}_{\{t \in T_i^w\}}, j = 1, 2, \dots m,$$
 (13)

where  $\mathbb{I}_{\{A\}}$  is the indicator of event A, indicating that, the camera pose is fixed each waypoint time interval  $T_j^w = [\frac{j-1}{m}, \frac{j}{m}]$ . In total, we select m=100 waypoints in each

![](_page_5_Figure_0.jpeg)

Fig. 6: We visualize the smooth trajectory the camera moves in for each of the three Gaussian Splatting models. The positions of the Gaussians in the reconstruction are illustrated in red.

trajectory. Waypoint representation provides a simple and deterministic method to create a piece-wise constant representation of the camera's pose over time.

*2) Polynomial Representation:* We define our trajectory as a third-order polynomial of time. The polynomial basis function can be defined as

$$\psi(t) = [t^0, t^1, t^2, \dots, t^{N-1}]^\top, \tag{14}$$

where t is the input variable and N is the number of the max order. In our experiment, we selected N = 6 to strike a balance between over-fitting and under-fitting.

Metrics: We evaluate the quality of the image sequence and how smoothly the motion trajectory moves through the environment reconstruction. Intersection of Union: Intersection of Union (IoU) is a metric for ensuring that the camera's path is optimized to capture objects accurately and consistently. The IoU score is calculated as the ratio of the area of intersection between the predicted and ground truth bounding boxes to the area of their union. This score ranges from 0 to 1, where a score of 1 indicates a perfect overlap and a score of 0 indicates no overlap at all. Log Dimensionless Jerk: Log Dimensionless Jerk (LDJ) [37] is a measure used to quantify the smoothness of a motion trajectory, by considering the third derivative of motion. We seek to ensure that the generated trajectory moves smoothly across the scene.

## *D. Analysis of Empirical Results*

We provide an analysis of our results against our baselines.

Waypoint: The waypoint representation results in overfitting — it causes discontinuities between intervals. This occurs because randomly initialized waypoints struggle to converge to a single optimal pose when multiple optima exist in the cost manifold. This can result in larger angular and positional jerks, leading to non-smooth trajectories that may cause failures in downstream robotics tasks.

Polynomial: While polynomial representation offers smoother trajectories compared to other methods, the limited variability of the sixth-order polynomial trajectory often results in sub-optimal poses. Experiments show that the angular and positional variations in optimized polynomial trajectories are insufficient to avoid occlusions, as indicated by the low IoU score in Table [II.](#page-5-0) Additionally, the noticeable stillness at the beginning and rapid motion near each trajectory's end, deteriorate the quality of the video.

<span id="page-5-0"></span>

|                                      |           | Trajectory Representation |               |                |  |
|--------------------------------------|-----------|---------------------------|---------------|----------------|--|
| Metrics/Scenarios                    |           | waypoints                 | polynomial    | RBF            |  |
| Avg.<br>target<br>centering<br>error | teatime   | 0.159 ± 0.075             | 0.143 ± 0.120 | 0.151 ± 0.159  |  |
|                                      | kitchen   | 0.145 ± 0.059             | 0.363 ± 0.277 | 0.228 ± 0.198  |  |
|                                      | figurines | 0.169 ± 0.072             | 0.140 ± 0.070 | 0.147 ± 0.192  |  |
| Avg.<br>target<br>ratio<br>error     | teatime   | 0.133 ± 0.056             | 0.115 ± 0.043 | 0.101 ± 0.040  |  |
|                                      | kitchen   | 0.125 ± 0.044             | 0.158 ± 0.042 | 0.118 ± 0.035  |  |
|                                      | figurines | 0.145 ± 0.050             | 0.159 ± 0.028 | 0.151 ± 0.026  |  |
| Avg. IoU                             | teatime   | 0.320 ± 0.265             | 0.531 ± 0.232 | 0.626 ± 0.178  |  |
|                                      | kitchen   | 0.313 ± 0.171             | 0.251 ± 0.216 | 0.525 ± 0.188  |  |
|                                      | figurines | 0.247 ± 0.267             | 0.325 ± 0.223 | 0.626 ± 0.178  |  |
| Angular<br>LDJ                       | Teatime   | 15.572 ± 0.650            | 7.567 ± 0.774 | 10.229 ± 0.599 |  |
|                                      | kitchen   | 15.942 ± 0.797            | 7.909 ± 0.965 | 10.357 ± 0.713 |  |
|                                      | figurines | 15.816 ± 0.615            | 7.513 ± 0.832 | 9.835 ± 0.586  |  |
| Positional<br>LDJ                    | Teatime   | 15.876 ± 0.710            | 7.550 ± 0.376 | 10.265 ± 0.711 |  |
|                                      | kitchen   | 16.144 ± 0.709            | 7.754 ± 0.848 | 10.610 ± 0.610 |  |
|                                      | figurines | 15.898 ± 0.613            | 7.777 ± 0.764 | 10.278 ± 0.431 |  |

TABLE II: Trajectory optimization results (mean ± S.D.): We compared the performance of trajectory representations (waypoints, polynomial, and RBF) across metrics and scenarios. The metrics include average target centering error, average target ratio error, average IoU, angular log dimensionless jerk (LDJ), and positional LDJ. The scenarios tested were teatime, kitchen, and figurines. The best-performing method for each metric and scenario is bold.

Radial Basis Function: In contrast, the RBF representation produces smooth and object-oriented trajectories. The high average IoU score suggests that RBF effectively finds occlusion-avoiding poses. In contrast, the low average ratio error and centering error indicate that the trajectory is wellcentered around the corresponding objects. Rendered images and 3D trajectories from each scenario, as visualized in Fig. [3,](#page-4-3) highlighted the trajectory generated by RBF. Compared to waypoint and polynomial representations, the RBF representation successfully provides trajectory transverse along the low-cost region defined by the optimization goal with a smooth transition between different objects.

# VI. CONCLUSIONS

In this work, we proposed SplaTraj, a framework that formalizes image sequence generation as a trajectory optimization problem. Specifically, SplaTraj enables users to specify regions and objects for the camera to visit semantically. We design costs on these 3D structures rendered to the view of a camera, which determines the desired positions within an image of the renderings. The trajectory optimizer subsequently differentiates through the rendering function and solves to obtain a continuous-time trajectory of camera poses. We empirically demonstrated that the rendering cost defined successfully leads to object-centered, properly distanced, and occlusion-avoiding rendered images, over multiple Gaussian Splatting scenes. Future avenues for research include adding further kinematics constraints into the trajectory optimization and extending SplaTraj to work in time-varying and dynamic Gaussian Splatting models.

# REFERENCES

- [1] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, "Nerf: Representing scenes as neural radiance fields for view synthesis," in *ECCV*, 2020.
- [2] B. Kerbl, G. Kopanas, T. Leimkuhler, and G. Drettakis, "3d gaussian ¨ splatting for real-time radiance field rendering," *ACM Transactions on Graphics*, 2023.
- [3] T. Zhang, K. Huang, W. Zhi, and M. Johnson-Roberson, "Darkgs: Learning neural illumination and 3d gaussians relighting for robotic exploration in the dark," *arXiv preprint*, 2024.
- [4] A. Elfes, "Sonar-based real-world mapping and navigation," *IEEE Journal on Robotics and Automation*, 1987.
- [5] W. Zhi, L. Ott, R. Senanayake, and F. Ramos, "Continuous occupancy map fusion with fast bayesian hilbert maps," in *International Conference on Robotics and Automation (ICRA)*, 2019.
- [6] H. Wright, W. Zhi, M. Johnson-Roberson, and T. Hermans, "V-prism: Probabilistic mapping of unknown tabletop scenes," *arXiv*, 2024.
- [7] R. Malladi, J. A. Sethian, and B. C. Vemuri, "Shape modeling with front propagation: a level set approach," *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 1995.
- [8] W. Zhi, R. Senanayake, L. Ott, and F. Ramos, "Spatiotemporal learning of directional uncertainty in urban environments with kernel recurrent mixture density networks," *IEEE Robotics and Automation Letters*, 2019.
- [9] W. Zhi, L. Ott, and F. Ramos, "Kernel trajectory maps for multi-modal probabilistic motion prediction," in *Conference on Robot Learning (CoRL)*, 2019.
- [10] T. Muller, A. Evans, C. Schied, and A. Keller, "Instant neural graphics ¨ primitives with a multiresolution hash encoding," *ACM Trans. Graph.*, 2022.
- [11] T. Zhang, W. Zhi, K. Huang, J. Mangelson, C. Barbalata, and M. Johnson-Roberson, "Recgs: Removing water caustic with recurrent gaussian splatting," *arXiv preprint arXiv:2407.10318*, 2024.
- [12] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, "Learning transferable visual models from natural language supervision," in *Proceedings of the 38th International Conference on Machine Learning*, vol. 139, pp. 8748–8763, 2021.
- [13] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, "Langsplat: 3d language gaussian splatting," 2024.
- [14] S. Fleishman, D. Cohen-Or, and D. Lischinski, "Automatic camera placement for image-based modeling," in *Proceedings of the conference on Visualization'99: celebrating ten years*, pp. 287–294, IEEE Computer Society Press, 1999.
- [15] O. S. Albahri, "Simulation-based optimization for camera placement in buildings," *Automation in Construction*, vol. 81, pp. 286–299, 2017.
- [16] R. Bodor, A. Drenner, M. Janssen, P. Schrater, and N. Papanikolopoulos, "Mobile camera positioning to optimize the observability of human activity recognition tasks," in *Proceedings of the IEEE International Conference on Advanced Video and Signal Based Surveillance*, pp. 552–557, 2005.
- [17] S. M. LaValle, *Planning Algorithms*. USA: Cambridge University Press, 2006.
- [18] I. A. S¸ucan, M. Moll, and L. E. Kavraki, "The Open Motion Planning Library," *IEEE Robotics & Automation Magazine*, pp. 72–82, December 2012.
- [19] T. Lai, W. Zhi, T. Hermans, and F. Ramos, "Parallelised diffeomorphic sampling-based motion planning," in *Conference on Robot Learning (CoRL)*, 2021.
- [20] J. Schulman, J. Ho, A. X. Lee, I. Awwal, H. Bradlow, and P. Abbeel, "Finding locally optimal, collision-free trajectories with sequential convex optimization," in *Robotics: Science and Systems*, 2013.
- [21] N. Ratliff, M. Zucker, J. A. Bagnell, and S. Srinivasa, "Chomp: Gradient optimization techniques for efficient motion planning," in *IEEE International Conference on Robotics and Automation*, 2009.
- [22] M. Kalakrishnan, S. Chitta, E. Theodorou, P. Pastor, and S. Schaal, "Stomp: Stochastic trajectory optimization for motion planning," *IEEE International Conference on Robotics and Automation*, 2011.
- [23] M. Neunert, C. de Crousaz, F. Furrer, M. Kamel, F. Farshidian, R. Siegwart, and J. Buchli, "Fast nonlinear model predictive control for unified trajectory optimization and tracking," *2016 IEEE International Conference on Robotics and Automation (ICRA)*, 2016.

- [24] G. Williams, P. Drews, B. Goldfain, J. M. Rehg, and E. Theodorou, "Aggressive driving with model predictive path integral control," in *IEEE International Conference on Robotics and Automation (ICRA)*, 2016.
- [25] N. D. Ratliff, J. Issac, D. Kappler, S. Birchfield, and D. Fox, "Riemannian motion policies," *CoRR*, 2018.
- [26] K. Van Wyk, M. Xie, A. Li, M. A. Rana, B. Babich, B. Peele, Q. Wan, I. Akinola, B. Sundaralingam, D. Fox, B. Boots, and N. D. Ratliff, "Geometric fabrics: Generalizing classical mechanics to capture the physics of behavior," *IEEE Robotics and Automation Letters*, 2022.
- [27] W. Zhi, I. Akinola, K. van Wyk, N. Ratliff, and F. Ramos, "Global and reactive motion generation with geometric fabric command sequences," in *IEEE International Conference on Robotics and Automation, ICRA*, 2023.
- [28] W. Zhi, T. Lai, L. Ott, E. V. Bonilla, and F. Ramos, "Learning efficient and robust ordinary differential equations via invertible neural networks," in *International Conference on Machine Learning, ICML*, 2022.
- [29] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, "Learning transferable visual models from natural language supervision," *CoRR*, 2021.
- [30] Y. Zheng, X. Chen, Y. Zheng, S. Gu, R. Yang, B. Jin, P. Li, C. Zhong, Z. Wang, L. Liu, C. Yang, D. Wang, Z. Chen, X. Long, and M. Wang, "Gaussiangrasper: 3d language gaussian splatting for open-vocabulary robotic grasping," *CoRR*, 2024.
- [31] J. Kerr, C. M. Kim, K. Goldberg, A. Kanazawa, and M. Tancik, "Lerf: Language embedded radiance fields," 2023.
- [32] M. Ester, H.-P. Kriegel, J. Sander, X. Xu, *et al.*, "A density-based algorithm for discovering clusters in large spatial databases with noise.," in *kdd*, vol. 96, pp. 226–231, 1996.
- [33] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," 2017.
- [34] M. ul Islam Arif, M. Jameel, and L. Schmidt-Thieme, "Directly optimizing iou for bounding box localization," 2023.
- [35] M. Welling and Y. W. Teh, "Bayesian learning via stochastic gradient langevin dynamics," in *Proceedings of the 28th International Conference on International Conference on Machine Learning*, 2011.
- [36] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization," in *International Conference on Learning Representations*, 2015.
- [37] N. Hogan and D. Sternad, "Sensitivity of smoothness measures to movement duration, amplitude, and arrests," *Journal of Motor Behavior*, vol. 41, no. 6, 2009.