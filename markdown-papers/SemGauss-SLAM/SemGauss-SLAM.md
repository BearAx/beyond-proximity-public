# SemGauss-SLAM: Dense Semantic Gaussian Splatting SLAM

Siting Zhu<sup>1</sup>, Renjie Qin<sup>1</sup>, Guangming Wang<sup>2</sup>, Jiuming Liu<sup>1</sup>, Hesheng Wang<sup>1</sup>

Abstract—We propose SemGauss-SLAM, a dense semantic SLAM system utilizing 3D Gaussian representation, that enables accurate 3D semantic mapping, robust camera tracking, and high-quality rendering simultaneously. In this system, we incorporate semantic feature embedding into 3D Gaussian representation, which effectively encodes semantic information within the spatial layout of the environment for precise semantic scene representation. Furthermore, we propose feature-level loss for updating 3D Gaussian representation, enabling higherlevel guidance for 3D Gaussian optimization. In addition, to reduce cumulative drift in tracking and improve semantic reconstruction accuracy, we introduce semantic-informed bundle adjustment. By leveraging multi-frame semantic associations, this strategy enables joint optimization of 3D Gaussian representation and camera poses, resulting in low-drift tracking and accurate semantic mapping. Our SemGauss-SLAM demonstrates superior performance over existing radiance fieldbased SLAM methods in terms of mapping and tracking accuracy on Replica and ScanNet datasets, while also showing excellent capabilities in high-precision semantic segmentation and dense semantic mapping. Code will be available at https://github.com/IRMVLab/SemGauss-SLAM.

#### I. INTRODUCTION

Dense semantic Simultaneous Localization and Mapping (SLAM) is a fundamental challenge for robotic systems [1], [2] and autonomous driving [3], [4]. It integrates semantic understanding of the environment into dense map reconstruction and performs pose estimation simultaneously. Traditional dense semantic SLAM has limitations including its inability to predict unknown areas [5]. Subsequent semantic SLAM based on Neural Radiance Fields (NeRF) [6] methods [7], [8], [9] have addressed these drawbacks, but suffer from inefficient per-pixel raycasting rendering for real-time optimization of implicit scene representation and low-quality novel view semantic representation.

Recently, a novel radiance field based on 3D Gaussian Splatting (3DGS) [10] has demonstrated remarkable capability in scene representation, enabling high-quality and efficient rendering via splatting. Following the advantages of 3D Gaussian representation, 3DGS-based SLAM methods [11], [12], [13], [14], [15] have been developed to achieve photorealistic mapping. However, most existing 3DGS SLAM systems focus on visual mapping to obtain RGB maps, where color information alone is insufficient for downstream tasks

![](_page_0_Figure_10.jpeg)

Fig. 1. Our SemGauss-SLAM incorporates semantic feature embedding into 3D Gaussian representation to perform dense semantic SLAM. This modeling strategy not only achieves accurate semantic mapping, but also enables high-precision semantic novel view synthesis compared with other radiance field-based semantic SLAM. We visualize 3D Gaussian blobs with semantic embedding, showing the spatial layout of semantic Gaussian representation. Moreover, semantic mapping is visualized using semantic feature embedding, showing 3D semantic modeling of the scene.

such as navigation. Moreover, current semantic NeRF-based SLAM methods suffer from cumulative drift in tracking, leading to degraded SLAM accuracy. Additionally, these methods struggle to achieve accurate semantic segmentation from novel viewpoints, indicating limited precision in online-reconstructed 3D semantic representation. Therefore, developing a low-drift and high-precision semantic SLAM system based on radiance field is essential and challenging.

To overcome this challenge, we introduce a novel dense semantic SLAM system based on 3D Gaussian Splatting with semantic-informed bundle adjustment, which enables high accuracy in tracking, dense mapping, and semantic segmentation from novel view. Different from concurrent work SGS-SLAM [16], which uses color for semantic representation to achieve 3DGS semantic SLAM, our method integrates semantic feature embedding into 3D Gaussian for semantic modeling, resulting in a more discriminative and comprehensive understanding of the scene. Moreover, by leveraging the explicit 3D structure of 3D Gaussian representation, our embedding-based semantic Gaussian representation is capable of capturing the spatial distribution of semantic information, achieving high-accuracy novel view semantic segmentation. Furthermore, to reduce accumulated drift in radiance field-based semantic SLAM, we leverage semantic associations among co-visible frames and propose semantic-informed bundle adjustment (BA) for joint optimization of camera poses and 3D Gaussian representation. This design exploits the consistency of multi-view semantics for establishing constraints, which enables the reduction of

<sup>\*</sup>This work was supported in part by the Natural Science Foundation of China under Grant 62225309, U24A20278, 62361166632, U21A20480 and 62403311. Corresponding Author: Hesheng Wang (wanghesheng@sjtu.edu.cn).

<sup>&</sup>lt;sup>1</sup>School of Automation and Intelligent Sensing, Key Laboratory of System Control and Information Processing, Ministry of Education of China, Shanghai Jiao Tong University, Shanghai.

<sup>&</sup>lt;sup>2</sup> University of Cambridge, United Kingdom.

cumulative drift in tracking and enhanced semantic mapping precision. Overall, we provide the following contributions:

- We present SemGauss-SLAM, a dense semantic SLAM system based on 3D Gaussian, which can achieve accurate semantic mapping, photo-realistic reconstruction, and robust tracking. We incorporate semantic feature embedding into 3D Gaussian to achieve precise semantic scene representation. Moreover, feature-level loss is introduced to provide higher-level guidance for 3D Gaussian optimization, leading to high-precision scene optimization results.
- We perform semantic-informed bundle adjustment by leveraging multi-view semantic constraints for joint optimization of camera poses and 3D Gaussian representation, achieving low-drift tracking and accurate semantic mapping.
- We conduct extensive evaluations on challenging datasets, to demonstrate our method achieves superior performance compared with existing radiance fieldbased SLAM in mapping, tracking, semantic segmentation, and novel-view synthesis.

## II. RELATED WORKS

Traditional Semantic SLAM. Traditional semantic SLAM employs explicit 3D representation such as surfels [2], mesh [1], [17], [18] and Truncated Signed Distance Fields (TSDF) [19], [20], [21] for dense semantic mapping. SemanticFusion [2] uses surfel representation and employs Conditional Random Field (CRF) for updating class probability distribution incrementally. Fusion++ [20] performs object-level SLAM where each object is reconstructed within its own TSDF volume and segmented based on estimated foreground probability. Kimera [1] utilizes visual-inertial odometry for pose estimation and generates dense semantic mesh maps. However, these explicit scene modeling methods not only require high storage space but also fail to achieve high-fidelity and complete 3D reconstruction.

Neural Implicit SLAM. Neural implicit representation [6] has shown promising capability in scene reconstruction for dense mapping. iMAP [22] first achieves mapping and tracking utilizing a single MLP network for scene representation. To overcome over-smoothed scene reconstruction and improve scalability, NICE-SLAM [23] adopts hierarchical feature grid representation. Following this, several works [24], [25], [26], [27], [28], [29] introduce more efficient scene representation, such as hash-based feature grid and feature plane, to achieve more accurate SLAM performance.

For neural implicit semantic SLAM, DNS SLAM [8] utilizes 2D semantic priors and integrates multi-view geometry constraints for semantic reconstruction. SNI-SLAM [7] introduces feature collaboration and one-way correlation decoder for improved scene representation in semantic mapping. However, these methods require specific scene bounds for mapping and suffer from cumulative drift in pose estimation. In this paper, we leverage the explicit structure of 3D Gaussian for unbounded mapping and perform semanticinformed bundle adjustment utilizing multi-frame semantic constraints for conducting low-drift and high-quality dense semantic SLAM.

3D Gaussian Splatting SLAM. 3D Gaussian Splatting [10] emerges as a promising 3D scene representation using a set of 3D Gaussians with learnable properties, including 3D center position, anisotropic covariance, opacity, and color. This representation is capable of quick differential rendering through splatting and has a wide range of applications in dynamic scene modeling [30], [31], semantic segmentation [32], [33] and scene editing [34].

Our main focus is on 3D Gaussian SLAM [11], [12], [14], [13]. These works emerge concurrently and all perform dense visual SLAM by leveraging scene geometry and appearance modeling capabilities of 3D Gaussian representation. SplaTAM [12] introduces silhouette-guided optimization to facilitate structured map expansion for dense mapping of visual SLAM. Gaussian Splatting SLAM [14] performs novel Gaussian insertion and pruning for monocular SLAM. However, the capability of 3D Gaussian representation extends well beyond appearance and geometry modeling of the scene, as it can be augmented to perform semantic scene understanding. The concurrent work SGS-SLAM [16] introduces semantic color associated with the Gaussian for semantic representation. However, this color-based semantic modeling method ignores the higher-level information inherent in semantics, which is insufficient for semantic representation of the environment. To address this limitation, we incorporate semantic feature embedding into 3D Gaussian for 3D semantic scene modeling to achieve high-precision dense semantic SLAM.

## III. METHOD

The overview of SemGauss-SLAM is shown in Fig. [2.](#page-2-0) Sec. [III-A](#page-1-0) introduces semantic Gaussian representation for dense semantic mapping, as well as the process of 3DGSbased semantic SLAM. Sec. [III-B](#page-3-0) introduces loss functions in the mapping and tracking process. Sec. [III-C](#page-3-1) presents semantic-informed bundle adjustment to reduce accumulated drift in tracking and improve mapping accuracy.

### <span id="page-1-0"></span>*A. 3D Gaussian Semantic Mapping and Tracking*

Semantic Gaussian Representation. We utilize a set of isotropy Gaussians with specific properties for scene representation in SLAM. To achieve semantic Gaussian mapping, we introduce a new parameter, semantic feature embedding, to each Gaussian for semantic representation. This design enables compact and efficient Gaussian semantic representation to capture the spatial semantic information of the environment. Moreover, it is crucial for 3D Gaussian representation, augmented by semantic feature embedding, to converge rapidly during optimization process for realtime mapping. Therefore, instead of initializing these feature embeddings randomly, we propagate 2D semantic features extracted from images to 3D Gaussian as the initial values to achieve faster convergence of semantic Gaussian optimization. In this work, we use a universal feature extractor DINOv2 [35], followed by a pretrained classifier to construct

![](_page_2_Figure_0.jpeg)

<span id="page-2-0"></span>Fig. 2. An overview of SemGauss-SLAM. Our method takes an RGB-D stream as input. RGB images are fed into feature extractor to obtain semantic features. These features are then categorized by a pretrained classifier to attain semantic labels. Then, semantic features, semantic labels, along with the input RGB and depth data serve as supervision signals. In the meantime, semantic features and input RGB-D data propagate to 3D Gaussian blobs as initial properties of Gaussian representation. Rendered semantic features, RGB, and depth are obtained from 3D Gaussian splatting, while rendered semantic labels are attained by classifying rendered features. Supervision and rendered information are utilized for loss construction to optimize camera poses and 3D Gaussian representation. During the SLAM process, we utilize semantic-informed bundle adjustment based on multi-frame constraints for joint optimization of poses and 3D Gaussian representation.

the segmentation network. Overall, each Gaussian includes 3D center position  $\mu$ , radius r, color c=(r,g,b), opacity  $\alpha$ , 16-channel semantic feature embedding e, and is defined as standard Gaussian equation multiplied by opacity  $\alpha$ :

<span id="page-2-1"></span>
$$g(x) = \alpha \exp\left(-\frac{\|x - \mu\|^2}{2r^2}\right). \tag{1}$$

**3D Gaussian Rendering.** Following Gaussian splatting [10], we project 3D Gaussians to 2D splats for high-fidelity differentiable rendering, which facilitates explicit gradient flow for Gaussian scene optimization and pose estimation. Specifically, for splatting of semantic feature embedding, we first sort all Gaussians in order of depth from near to far and then blend N ordered points projecting to pixel p = (u, v), obtaining 2D semantic feature maps E(p):

<span id="page-2-2"></span>
$$E(p) = \sum_{i \in N} e_i g_i(p) \prod_{j=1}^{i-1} (1 - g_j(p)),$$
 (2)

where  $g_i(p)$  is computed as shown in Eq.(1) with  $\mu$  and r representing the rendered 2D Gaussians in pixel plane:

$$\mu_{\text{pix}} = K_c \frac{T_k \mu}{d}, \ r_{\text{pix}} = \frac{fr}{d}, \ \text{where } d = (T_k \mu)_z.$$
 (3)

 $K_c$  is calibrated camera intrinsic,  $T_k$  is estimated camera pose at frame k, f is known focal length, d is the depth of the i-th Gaussian in camera coordinates.

For RGB and depth rendering, we follow the similar approach in Eq.(2):

$$C(p) = \sum_{i \in N} c_i g_i(p) \prod_{j=1}^{i-1} (1 - g_j(p)),$$

$$D(p) = \sum_{i \in N} d_i g_i(p) \prod_{j=1}^{i-1} (1 - g_j(p))$$
(4)

where C(p) and D(p) represents splatted 2D color and depth images respectively. Moreover, given the camera pose, visibility information of Gaussian is required for mapping and tracking process, such as adding new Gaussian and loss construction. Therefore, following [12], we render a silhouette image to determine visibility:

$$Sil(p) = \sum_{i \in N} g_i(p) \prod_{i=1}^{i-1} (1 - g_j(p)).$$
 (5)

**Tracking Process.** During tracking process, we keep 3D Gaussian parameters fixed and only optimize camera pose of current frame. Since the proximity between adjacent frames is relatively small, we assume a constant velocity model to obtain an initial pose estimation for the current frame. The camera pose is then iteratively refined through optimization by minimizing the loss between two components: differentiable rendering from 3D Gaussian representation and camera observation within the visible silhouette.

Mapping Process. Our system performs RGB mapping and semantic mapping simultaneously. Mapping process begins with the initialization of the scene representation, which is achieved by inverse transforming all pixels of the first frame to 3D coordinates and obtaining the initial 3D Gaussian representation. Then, when the overlap of coming frame with rendering of the existing map is less than half, we add a new Gaussian for incremental mapping.

### <span id="page-3-0"></span>*B. Loss Functions*

For optimization of semantic scene representation, we utilize cross-entropy loss for constructing semantic loss Ls. Furthermore, instead of solely using semantic loss for optimization, we introduce a feature-level loss L<sup>f</sup> for higherlevel guidance of semantic optimization:

$$\mathcal{L}_f = \sum_{p \in P_M} |F_e - E(p)|,\tag{6}$$

where F<sup>e</sup> is extracted features generated by DINOv2 [35] based feature extractor. P<sup>M</sup> represents a set of all pixels in the rendered image. Compared with semantic loss, feature loss offers explicit supervision on intermediate features for semantic Gaussian optimization, leading to more robust and accurate semantic understanding of the scene.

We employ RGB loss L<sup>c</sup> and depth loss L<sup>d</sup> for optimizing scene color and geometry representation. L<sup>c</sup> and L<sup>d</sup> are both L1 loss constructed by comparing the RGB and depth splats with the input RGB-D frame. These loss functions are then utilized for mapping and pose estimation.

In the mapping process, we construct loss over all rendered pixels for 3D Gaussian optimization. Moreover, we add SSIM term to RGB loss following [10]. The complete loss function for mapping is a weighted sum of the above losses:

$$\mathcal{L}_{\text{mapping}} = \sum_{p \in P_M} (\lambda_{f_m} \mathcal{L}_f(p) + \lambda_{s_m} \mathcal{L}_s(p) + \lambda_{c_m} \mathcal{L}_c(p) + \lambda_{d_m} \mathcal{L}_d(p)). \tag{7}$$

λfm, λsm, λcm, λd<sup>m</sup> are weighting coefficients.

In the tracking process, using an overly constrained loss function for pose estimation can lead to decreased accuracy in camera pose and increased processing time. Therefore, loss function for tracking is constructed based only on a weighted sum of RGB loss and depth loss:

$$\mathcal{L}_{\text{tracking}} = \sum_{p \in P_T} (\lambda_{c_t} \mathcal{L}_c(p) + \lambda_{d_t} \mathcal{L}_d(p)), \tag{8}$$

where λ<sup>c</sup><sup>t</sup> , λ<sup>d</sup><sup>t</sup> are weighting coefficients in tracking process. P<sup>T</sup> represents pixels that are rendered from well-optimized part of 3D Gaussian map, which is area that rendered visibility silhouette Sil(p) is greater than 0.99.

### <span id="page-3-1"></span>*C. Semantic-informed Bundle Adjustment*

Currently, existing radiance field-based semantic SLAM systems utilize the latest input RGB-D frame to construct RGB and depth loss for pose estimation. Subsequently, the scene representation of these SLAM systems is optimized using the estimated pose and the latest frame. However, relying solely on single-frame constraint for pose optimization can lead to cumulative drift in the tracking process due to the absence of global constraints. Furthermore, using only single-frame information to optimize scene representation can result in globally inconsistent updates to the scene on the semantic level. To address this problem, we propose semantic-informed bundle adjustment to achieve joint optimization of 3D Gaussian representation and camera poses by leveraging multi-view constraints and semantic associations.

In semantic-informed BA, we leverage the consistency of multi-view semantics to establish constraints. Specifically, rendered semantic feature is warped to its co-visible frame j using estimated relative pose transformation T j i , and constructs loss with rendered semantic feature G(T<sup>j</sup> , e) of frame j to obtain LBA-sem:

<span id="page-3-2"></span>
$$\mathcal{L}_{\text{BA-sem}} = \sum_{i=1}^{N-1} \sum_{j=i+1}^{N} (|T_i^j \cdot \mathcal{G}(T_i, e) - \mathcal{G}(T_j, e)|), \quad (9)$$

where G(T<sup>i</sup> , e) represents splatted semantic embedding from 3D Gaussian G using camera pose T<sup>i</sup> . Moreover, to achieve geometry and appearance consistency, we also warp rendered RGB and depth to co-visible frames to construct loss with corresponding frames following similar approach in Eq.[\(9\)](#page-3-2):

$$\mathcal{L}_{\text{BA-rgb}} = \sum_{i=1}^{N-1} \sum_{j=i+1}^{N} (|T_i^j \cdot \mathcal{G}(T_i, c) - \mathcal{G}(T_j, c)|),$$

$$\mathcal{L}_{\text{BA-depth}} = \sum_{i=1}^{N-1} \sum_{j=i+1}^{N} (|T_i^j \cdot \mathcal{G}(T_i, d) - \mathcal{G}(T_j, d)|), \quad (10)$$

where G(T<sup>i</sup> , c) and G(T<sup>i</sup> , d) represents rendered RGB and depth of frame i. Therefore, overall loss function LBA for joint optimization of corresponding frame poses and 3D Gaussian scene representation is the weighted sum of the above losses:

$$\mathcal{L}_{\text{BA}} = \lambda_e \mathcal{L}_{\text{BA-sem}} + \lambda_c \mathcal{L}_{\text{BA-rgb}} + \lambda_d \mathcal{L}_{\text{BA-depth}}, \tag{11}$$

where λe, λc, λ<sup>d</sup> are weighting coefficients. This design leverages the fast rendering capability of 3D Gaussian to achieve joint optimization of scene representation and camera poses. Furthermore, semantic-informed BA integrates consistency and correlation of multi-perspective semantic, geometry, and appearance information, resulting in low-drift tracking and consistent mapping.

## IV. EXPERIMENTS

### *A. Experimental Setup*

Datasets. We evaluate the performance of SemGauss-SLAM on two datasets with semantic ground truth annotations, including 8 scenes on simulated dataset Replica [36] and 5 scenes on real-world dataset ScanNet [37].

Metrics. We follow metrics from [12] to evaluate the SLAM system accuracy and rendering quality. For reconstruction metric, we use *Depth L1 (cm)*. For tracking accuracy evaluation, we use *ATE RMSE (cm)* [38]. Moreover, we use *PSNR (dB)*, *SSIM*, and *LPIPS* for evaluating RGB image rendering performance. Semantic segmentation is evaluated with respect to *mIoU (%)* metric.

![](_page_4_Figure_0.jpeg)

<span id="page-4-1"></span>Fig. 3. Qualitative comparison on rendering quality of our method and baseline. We visualize 5 selected scenes of Replica [36] and ScanNet [37] dataset. Details are highlighted with red color boxes. Our method achieves photo-realistic rendering quality and higher completion of reconstruction, especially in areas with rich textural information.

![](_page_4_Figure_2.jpeg)

<span id="page-4-2"></span>Fig. 4. Qualitative comparison on semantic novel view synthesis on 3 scenes of Replica [36].

**Baselines.** We compare our method with the existing state of-the-art dense visual SLAM, including NeRF-based SLAM [23], [26], [25], [27], [24] and 3DGS-based SLAM [12]. For comparison of dense semantic SLAM performance, we consider NeRF-based semantic SLAM [7], [8], [9], and SGS-SLAM [16] which is a work parallel to ours, as baseline.

**Implementation Details.** We run SemGauss-SLAM on NVIDIA RTX 4090 GPU. For experimental settings, we perform mapping every 8 frames. Weighting coefficients of each loss are  $\lambda_{f_m}=0.01,\,\lambda_{s_m}=0.01,\,\lambda_{c_m}=0.5,\,\lambda_{d_m}=1$  in mapping,  $\lambda_{c_t}=0.5$  and  $\lambda_{d_t}=1$  in tracking. Moreover, we set  $\lambda_e=0.004,\,\lambda_c=0.5,\,\lambda_c=1$  in semantic-informed bundle adjustment. The above weighting coefficients are set

<span id="page-4-0"></span>TABLE I

COMPARISON OF SLAM ACCURACY AND RENDERING PERFORMANCE.

RESULTS ARE AN AVERAGE OF 8 SCENES ON REPLICA DATASET [36]

| Methods              | Reconstruction<br>Depth L1[cm]↓ | Localization<br>RMSE[cm]↓ | Rendering Quality PSNR↑ SSIM↑ LPIPS |       |       |
|----------------------|---------------------------------|---------------------------|-------------------------------------|-------|-------|
| NICE-SLAM [23]       | 2.97                            | 2.51                      | 24.42                               | 0.809 | 0.233 |
| Vox-Fusion [24]      | 2.46                            | 1.47                      | 24.41                               | 0.801 | 0.236 |
| Co-SLAM [26]         | 1.51                            | 1.06                      | 30.24                               | 0.939 | 0.252 |
| ESLAM [25]           | 0.95                            | 0.62                      | 29.08                               | 0.929 | 0.239 |
| SplaTAM [12]         | 0.73                            | 0.41                      | 34.11                               | 0.968 | 0.102 |
| SNI-SLAM [7]         | 0.77                            | 0.46                      | 29.43                               | 0.935 | 0.235 |
| SemGauss-SLAM (Ours) | 0.50                            | 0.33                      | 35.03                               | 0.982 | 0.062 |

based on the numerical scale of different losses.

### B. Experimental Results

SLAM and Rendering Quality Results. As shown in Tab. I, our method achieves the highest accuracy in all metrics compared with other radiance field-based SLAM and up to 35% relative increase in reconstruction accuracy. This enhancement is attributed to the incorporation of semantic-informed bundle adjustment, which provides multiview constraint to achieve joint optimization of both camera poses and scene representation. Tab. II demonstrates our method outperforms baseline methods on real-world dataset ScanNet [37]. Note that each scene is tested and averaged with five independent runs to ensure the reliability of results. Novel View Semantic Evaluation Results. Tab. III shows that our method achieves up to 49% relative increase in semantic novel view synthesis compared with SNI-SLAM [7], showing excellent 3D semantic mapping accuracy. Note that for one scene, we randomly choose 100 new viewpoints

<span id="page-5-0"></span>TABLE II ACCURACY COMPARISON ON SCANNET DATASET [37] FOR TRACKING METRIC RMSE (cm)  $\downarrow$ .

| Methods              | 0000  | 0059  | 0169  | 0181  | 0207 | Avg.  |
|----------------------|-------|-------|-------|-------|------|-------|
| NICE-SLAM [23]       | 12.00 | 14.00 | 10.90 | 13.40 | 6.20 | 11.30 |
| Vox-Fusion [24]      | 68.84 | 24.18 | 27.28 | 23.30 | 9.41 | 30.60 |
| Point-SLAM [27]      | 10.24 | 7.81  | 22.16 | 14.77 | 9.54 | 12.90 |
| SplaTAM [12]         | 12.83 | 10.10 | 12.08 | 11.10 | 7.46 | 10.71 |
| SemGauss-SLAM (Ours) | 11.87 | 7.97  | 8.70  | 9.78  | 8.97 | 9.46  |
|                      |       |       |       |       |      |       |

TABLE III

<span id="page-5-1"></span>QUANTITATIVE COMPARISON OF SEMANTIC NOVEL VIEW SYNTHESIS PERFORMANCE ON REPLICA [36] FOR SEMANTIC METRIC mIoU(%).

| Methods              | room0        | room1        | room2        | office0      | Avg.         |
|----------------------|--------------|--------------|--------------|--------------|--------------|
| SNI-SLAM [7]         | 51.20        | 50.10        | 54.80        | 70.21        | 56.58        |
| SemGauss-SLAM (Ours) | <b>89.63</b> | <b>84.72</b> | <b>86.51</b> | <b>93.60</b> | <b>88.62</b> |

that are different from SLAM mapping perspectives for evaluation and mIoU is calculated between splatted semantic labels and ground truth labels. By introducing Gaussian feature embedding for semantic representation, our method enables continuous semantic modeling. This modeling is crucial for generating semantically coherent scenes, as it reduces the occurrence of sharp transitions that can cause inconsistencies, ensuring accurate semantic representation from novel viewpoints.

Semantic Segmentation Results. Since [9], [8], [16], [7] employs ground truth labels for supervision, for a fair comparison, we also present our results using ground truth labels for supervision, denoted as Our (GT). The results of using semantic segmentation results for supervision are Ours. As shown in Tab. IV, our work outperforms existing radiance field-based semantic SLAM methods. Such enhancement attributes to the integration of semantic feature embedding into 3D Gaussian for enriched semantic representation, and semantic feature-level loss for direct guidance of semantic optimization. Moreover, our proposed semantic-informed BA also contributes to high semantic precision, as it leverages multiple co-visible frames to construct a globally consistent semantic map for high-precision semantic representation.

**Visualization.** Fig. 3 shows rendering quality comparison of 4 scenes with interesting regions highlighted with colored boxes. For less-frequent observed areas, such as floor and side of sofa, other methods either result in low-quality reconstruction or leave holes. Our method leverages the high-quality rendering capability of 3D Gaussian representation and introduces semantic-informed BA to achieve detailed

<span id="page-5-2"></span>TABLE IV INPUT VIEWS SEMANTIC SEGMENTATION PERFORMANCE ON 4 SCENES OF REPLICA [36] FOR SEMANTIC METRIC mloU(%).

|     | Methods       | room0 | room1 | room2 | office0 | Avg.  |
|-----|---------------|-------|-------|-------|---------|-------|
|     | NIDS-SLAM [9] | 82.45 | 84.08 | 76.99 | 85.94   | 82.37 |
|     | DNS SLAM [8]  | 88.32 | 84.90 | 81.20 | 84.66   | 84.77 |
| GT  | SNI-SLAM [7]  | 88.42 | 87.43 | 86.16 | 87.63   | 87.41 |
|     | SGS-SLAM [16] | 92.95 | 92.91 | 92.10 | 92.90   | 92.72 |
|     | Ours (GT)     | 96.30 | 95.82 | 96.51 | 96.72   | 96.34 |
| Seg | Ours          | 92.81 | 94.10 | 94.72 | 95.23   | 94.22 |

![](_page_5_Figure_10.jpeg)

<span id="page-5-4"></span>Fig. 5. Semantic rendering results and ground truth labels of feature-level loss ablation on two scenes of Replica [36].

<span id="page-5-3"></span>TABLE V
ABLATION STUDY OF OUR CONTRIBUTIONS ON REPLICA [36].

| Methods                  | RMSE ↓ | room0<br>Depth L1 ↓ | mIoU ↑ | RMSE ↓ | office1<br>Depth L1 ↓ | mIoU ↑ |
|--------------------------|--------|---------------------|--------|--------|-----------------------|--------|
| w/o feature-level loss   | 0.26   | 0.54                | 83.60  | 0.17   | 0.22                  | 80.13  |
| w/o semantic-informed BA | 0.35   | 0.70                | 90.10  | 0.21   | 0.30                  | 87.73  |
| SemGauss-SLAM (Ours)     | 0.26   | 0.54                | 92.81  | 0.17   | 0.22                  | 90.11  |

and complete geometric reconstruction results. Specifically, our method enhances multi-view geometry consistency by BA to ensure that the reconstructed geometry aligns accurately across all observed viewpoints, leading to precise and complete geometry reconstruction. As shown in Fig. 4, our method achieves superior novel view semantic segmentation accuracy compared with baseline SNI-SLAM [7]. It can be observed that SNI-SLAM struggles with segmenting ceilings in novel view synthesis as they are less frequently observed during the mapping process. Consequently, the ceiling features are poorly modeled in the semantic scene representation. Our method introduces semantic-informed BA to construct multi-view constraints, enabling areas that are sparsely observed to effectively utilize the limited information from co-visible frames, thus establishing sufficient constraints for accurate semantic reconstruction.

#### C. Ablation Study

We perform ablation study on two scenes of Replica dataset [36] in Tab. V to validate the effectiveness of feature-level loss and semantic-informed BA in SemGauss-SLAM. Moreover, ablation of semantic-informed BA component is conducted in Tab. VI.

**Feature-level Loss.** Tab. V shows that incorporating feature-level loss significantly enhances semantic segmentation performance, while having little effect on tracking and geometric reconstruction. This result occurs because feature-level loss influences only the optimization of semantic features, without affecting the optimization of geometry and pose estimation. As shown in Fig. 5, utilizing feature-level loss can achieve improved boundary segmentation and finer segmentation of small objects. This enhancement occurs because feature loss compels the scene representation to capture high-dimensional and direct information within the feature space, leading to the capability of distinguishing intricate details and subtle variations within the scene.

**Semantic-informed BA.** Tab. V shows that introducing semantic-informed BA leads to enhancements in tracking, reconstruction, and semantic segmentation. This improvement

#### TABLE VI

<span id="page-6-0"></span>Ablation study of semantic-informed BA on Replica [36]. (W/o semantic) without adding  $\mathcal{L}_{BA\text{-}sem}$ ; (W/o RGB and depth) without adding  $\mathcal{L}_{BA\text{-}rgb}$  and  $\mathcal{L}_{BA\text{-}depth}$ .

| Methods              | RMSE ↓ | room0<br>Depth L1 ↓ | mIoU ↑ | RMSE ↓ | office1<br>Depth L1 ↓ | mIoU ↑ |
|----------------------|--------|---------------------|--------|--------|-----------------------|--------|
| w/o semantic         | 0.35   | 0.66                | 90.15  | 0.20   | 0.24                  | 87.95  |
| w/o RGB and depth    | 0.31   | 0.70                | 92.01  | 0.18   | 0.28                  | 89.60  |
| SemGauss-SLAM (Ours) | 0.26   | 0.54                | 92.81  | 0.17   | 0.22                  | 90.11  |

is due to the joint optimization of camera poses and scene representation, which is informed by multi-view constraints. As shown in Tab. VI, lacking semantic constraint leads to a significant decrease in tracking performance compared with the absence of color and depth constraints. Such result suggests that multi-view semantic constraints provide more comprehensive and accurate information, due to the consistency of semantics across multiple perspectives. Moreover, the absence of semantic constraint can lead to reduced semantic precision, while lacking color and depth constraints results in decreased reconstruction accuracy.

#### V. CONCLUSION

We propose SemGauss-SLAM, a novel dense semantic SLAM system utilizing 3D Gaussian representation that enables dense visual mapping, robust camera tracking, and 3D semantic mapping of the whole scene. We incorporate semantic feature embedding into 3D Gaussian for Gaussian semantic representation for dense semantic mapping. Moreover, we propose feature-level loss for 3D Gaussian scene optimization to achieve accurate semantic representation. In addition, we introduce semantic-informed BA that enables joint optimization of camera poses and 3D Gaussian representation by establishing multi-view semantic constraints, resulting in low-drift tracking and precise mapping.

#### REFERENCES

- [1] A. Rosinol, M. Abate, Y. Chang, and L. Carlone, "Kimera: an opensource library for real-time metric-semantic localization and mapping," in 2020 IEEE International Conference on Robotics and Automation (ICRA). IEEE, 2020, pp. 1689–1696.
- [2] J. McCormac, A. Handa, A. Davison, and S. Leutenegger, "Semanticfusion: Dense 3d semantic mapping with convolutional neural networks," in 2017 IEEE International Conference on Robotics and automation (ICRA). IEEE, 2017, pp. 4628–4635.
- [3] Y. Bao, Z. Yang, Y. Pan, and R. Huan, "Semantic-direct visual odometry," *IEEE Robotics and Automation Letters*, vol. 7, no. 3, pp. 6718–6725, 2022.
- [4] K.-N. Lianos, J. L. Schonberger, M. Pollefeys, and T. Sattler, "Vso: Visual semantic odometry," in *Proceedings of the European conference* on computer vision (ECCV), 2018, pp. 234–250.
- [5] Z. Liu, F. Milano, J. Frey, R. Siegwart, H. Blum, and C. Cadena, "Unsupervised continual semantic adaptation through neural rendering," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 3031–3040.
- [6] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, "Nerf: Representing scenes as neural radiance fields for view synthesis," *Communications of the ACM*, vol. 65, no. 1, pp. 99–106, 2021.
- [7] S. Zhu, G. Wang, H. Blum, J. Liu, L. Song, M. Pollefeys, and H. Wang, "Sni-slam: Semantic neural implicit slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 167–21 177.

- [8] K. Li, M. Niemeyer, N. Navab, and F. Tombari, "Dns-slam: Dense neural semantic-informed slam," in 2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS). IEEE, 2024, pp. 7839–7846.
- [9] Y. Haghighi, S. Kumar, J. P. Thiran, and L. Van Gool, "Neural implicit dense semantic slam," arXiv preprint arXiv:2304.14560, 2023.
- [10] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, "3d gaussian splatting for real-time radiance field rendering," ACM Transactions on Graphics, vol. 42, no. 4, 2023.
- [11] C. Yan, D. Qu, D. Xu, B. Zhao, Z. Wang, D. Wang, and X. Li, "Gs-slam: Dense visual slam with 3d gaussian splatting," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 19595–19604.
- [12] N. Keetha, J. Karhade, K. M. Jatavallabhula, G. Yang, S. Scherer, D. Ramanan, and J. Luiten, "Splatam: Splat track & map 3d gaussians for dense rgb-d slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 357–21 366.
- [13] V. Yugay, Y. Li, T. Gevers, and M. R. Oswald, "Gaussian-slam: Photo-realistic dense slam with gaussian splatting," arXiv preprint arXiv:2312.10070, 2023.
- [14] H. Matsuki, R. Murai, P. H. Kelly, and A. J. Davison, "Gaussian splatting slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 18 039–18 048.
- [15] H. Huang, L. Li, H. Cheng, and S.-K. Yeung, "Photo-slam: Real-time simultaneous localization and photorealistic mapping for monocular stereo and rgb-d cameras," in *Proceedings of the IEEE/CVF Confer*ence on Computer Vision and Pattern Recognition, 2024, pp. 21584– 21593.
- [16] M. Li, S. Liu, H. Zhou, G. Zhu, N. Cheng, T. Deng, and H. Wang, "Sgs-slam: Semantic gaussian splatting for neural dense slam," in European Conference on Computer Vision. Springer, 2024, pp. 163– 179.
- [17] Y. Tian, Y. Chang, F. H. Arias, C. Nieto-Granda, J. P. How, and L. Carlone, "Kimera-multi: Robust, distributed, dense metric-semantic slam for multi-robot systems," *IEEE Transactions on Robotics*, vol. 38, no. 4, 2022.
- [18] N. Hughes, Y. Chang, and L. Carlone, "Hydra: A real-time spatial perception system for 3d scene graph construction and optimization," arXiv preprint arXiv:2201.13360, 2022.
- [19] L. Schmid, J. Delmerico, J. L. Schönberger, J. Nieto, M. Pollefeys, R. Siegwart, and C. Cadena, "Panoptic multi-tsdfs: a flexible representation for online multi-resolution volumetric mapping and longterm dynamic scene consistency," in 2022 International Conference on Robotics and Automation (ICRA). IEEE, 2022, pp. 8018–8024.
- [20] J. McCormac, R. Clark, M. Bloesch, A. Davison, and S. Leutenegger, "Fusion++: Volumetric object-level slam," in 2018 international conference on 3D vision (3DV). IEEE, 2018, pp. 32–41.
- [21] M. Grinvald, F. Furrer, T. Novkovic, J. J. Chung, C. Cadena, R. Siegwart, and J. Nieto, "Volumetric instance-aware semantic mapping and 3d object discovery," *IEEE Robotics and Automation Letters*, vol. 4, no. 3, pp. 3037–3044, 2019.
- [22] E. Sucar, S. Liu, J. Ortiz, and A. J. Davison, "imap: Implicit mapping and positioning in real-time," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2021, pp. 6229–6238.
- [23] Z. Zhu, S. Peng, V. Larsson, W. Xu, H. Bao, Z. Cui, M. R. Oswald, and M. Pollefeys, "Nice-slam: Neural implicit scalable encoding for slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2022, pp. 12786–12796.
- [24] X. Yang, H. Li, H. Zhai, Y. Ming, Y. Liu, and G. Zhang, "Vox-fusion: Dense tracking and mapping with voxel-based neural implicit representation," in 2022 IEEE International Symposium on Mixed and Augmented Reality (ISMAR). IEEE, 2022, pp. 499–507.
- [25] M. M. Johari, C. Carta, and F. Fleuret, "Eslam: Efficient dense slam system based on hybrid representation of signed distance fields," in Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023, pp. 17408–17419.
- [26] H. Wang, J. Wang, and L. Agapito, "Co-slam: Joint coordinate and sparse parametric encodings for neural real-time slam," in *Proceed*ings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 2023, pp. 13293–13302.
- [27] E. Sandström, Y. Li, L. Van Gool, and M. R. Oswald, "Point-slam: Dense neural point cloud-based slam," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 18 433–18 444.

- [28] X. Kong, S. Liu, M. Taher, and A. J. Davison, "vmap: Vectorised object mapping for neural field slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 952–961.
- [29] J. Hu, M. Mao, H. Bao, G. Zhang, and Z. Cui, "Cp-slam: Collaborative neural point-based slam system," *Advances in Neural Information Processing Systems*, vol. 36, 2024.
- [30] Y. Yan, H. Lin, C. Zhou, W. Wang, H. Sun, K. Zhan, X. Lang, X. Zhou, and S. Peng, "Street gaussians: Modeling dynamic urban scenes with gaussian splatting," in *European Conference on Computer Vision*. Springer, 2024, pp. 156–173.
- [31] X. Zhou, Z. Lin, X. Shan, Y. Wang, D. Sun, and M.-H. Yang, "Drivinggaussian: Composite gaussian splatting for surrounding dynamic autonomous driving scenes," in *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, 2024, pp. 21 634–21 643.
- [32] M. Ye, M. Danelljan, F. Yu, and L. Ke, "Gaussian grouping: Segment and edit anything in 3d scenes," in *European Conference on Computer Vision*. Springer, 2024, pp. 162–179.
- [33] S. Zhou, H. Chang, S. Jiang, Z. Fan, Z. Zhu, D. Xu, P. Chari, S. You, Z. Wang, and A. Kadambi, "Feature 3dgs: Supercharging 3d gaussian splatting to enable distilled feature fields," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 676–21 685.
- [34] J. Zhuang, D. Kang, Y.-P. Cao, G. Li, L. Lin, and Y. Shan, "Tipeditor: An accurate 3d editor following both text-prompts and imageprompts," *ACM Transactions on Graphics (TOG)*, vol. 43, no. 4, pp. 1–12, 2024.
- [35] M. Oquab, T. Darcet, T. Moutakanni, H. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby *et al.*, "Dinov2: Learning robust visual features without supervision," *arXiv preprint arXiv:2304.07193*, 2023.
- [36] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma *et al.*, "The replica dataset: A digital replica of indoor spaces," *arXiv preprint arXiv:1906.05797*, 2019.
- [37] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, "Scannet: Richly-annotated 3d reconstructions of indoor scenes," in *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2017, pp. 5828–5839.
- [38] J. Sturm, N. Engelhard, F. Endres, W. Burgard, and D. Cremers, "A benchmark for the evaluation of rgb-d slam systems," in *2012 IEEE/RSJ international conference on intelligent robots and systems*. IEEE, 2012, pp. 573–580.