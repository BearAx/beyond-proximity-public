## NEDS-SLAM: A Neural Explicit Dense Semantic SLAM Framework using 3D Gaussian Splatting

Yiming Ji, Yang Liu ∗ , Guanghu Xie, Boyu Ma, Zongwu Xie, and Hong Liu

*Abstract*—We propose NEDS-SLAM, a dense semantic SLAM system based on 3D Gaussian representation, that enables robust 3D semantic mapping, accurate camera tracking, and highquality rendering in real-time. In the system, we propose a Spatially Consistent Feature Fusion model to reduce the effect of erroneous estimates from pre-trained segmentation head on semantic reconstruction, achieving robust 3D semantic Gaussian mapping. Additionally, we employ a lightweight encoderdecoder to compress the high-dimensional semantic features into a compact 3D Gaussian representation, mitigating the burde n of excessive memory consumption. Furthermore, we leverage the advantage of 3D Gaussian splatting, which enables efficient and differentiable novel view rendering, and propose a Virtual Camera View Pruning method to eliminate outlier gaussians, thereby effectively enhancing the quality of scene representations. Our NEDS-SLAM method demonstrates competitive performance over existing dense semantic SLAM methods in terms of mappin g and tracking accuracy on Replica and ScanNet datasets, whil e also showing excellent capabilities in 3D dense semantic mapping.

*Index Terms*—3D Gaussian Splatting; Dense Semantic Mapping; Neural SLAM; 3D Reconstruction.

#### I. INTRODUCTION

Visual SLAM (Simultaneous Localization and Mapping) is a fundamental research problem in robotics, which involves simultaneously tracking the camera pose and incrementally constructing a map of an unknown environment [\[1\]](#page-7-0). Downstream tasks such as autonomous goal navigation, human-computer interaction, mixed reality (MR), and augmented reality (AR ) demand not only accurate camera pose tracking from SLAM systems but also robust and dense semantic reconstruction o f the environment. This research focuses on semantic RGBD-SLAM, which, in contrast to traditional SLAM, enables the identification, classification, and association of entities within a scene, ultimately generating a semantically-rich map.

Inspired by the success of NERF and 3D Gaussian Splatting (3DGS) in high-fidelity view synthesis, researchers have explored building end-to-end visual SLAM systems based on neural radiance fields. These novel SLAM architectures offer superior solutions compared to traditional algorithms in terms of surface continuity, memory requirements, and scene completion. Specifically, iMAP [ [2\]](#page-7-1) and NICE-SLAM [ [3\]](#page-7-2) leverage neural implicit fields for consistent geometry representation, while MonoGS [ [4](#page-7-3) ] and SplaTAM [ [5\]](#page-7-4) employ 3DGS to achieve photo-realistic mapping.

All authors are with State Key Laboratory of Robotics and Systems, Harbin Institute of Technology. Email: yimingji@stu.hit.edu.cn (Yiming Ji), liuyanghit@hit.edu.cn (Yang Liu).

Given continuous input of RGB-D frames, dense semantic SLAM aims to create a compact and dense 3D representation of the scene that includes accurate RGB information as well as dense semantic data. However, current state-ofthe-art semantic segmentation models are trained on large amounts of internet images, which are loosely related and time-independent. This leads to estimation errors such as semantic spatial inconsistency, which significantly impairs the density and completeness of semantic reconstruction. The previous 3DGS-based semantic SLAM method [ [6\]](#page-7-5) overlooked the issue of semantic feature inconsistency, which limits its potential for practical applications.

1

Furthermore, our research has found that directly embeddin g semantic category labels into gaussians parameters may not be appropriate. During splatting, overlapping gaussians combine through alpha-blending to form pixel values on the imaging plane. Using RGB color channels as an example, ideally, when 3D gaussians are splatted onto different imaging planes, they create different color blending effects. However, assigning fixed class labels to the gaussians leads to meaningless values in the semantic channels during splatting. Therefore, attempting to embed semantic features instead of semantic category labels into the 3D gaussians parameters would be more promising. However, this approach can cause prohibitive memory requirements and significantly lower the efficiency o f both optimization and rendering, as semantic features typically have higher dimensions, whereas category labels are just integer values.

In a 3DGS-based SLAM system, the process of incrementally building a map is often influenced by camera pose estimation errors, object occlusions, and errors in the optimization process. These factors can introduce 3D gaussians that do no t align with actual surfaces. When these outlier gaussians ar e included in the rendering view, they can create visual artifacts, which in turn affect camera pose estimation, creating a vicious cycle. This issue is not addressed in the original 3DGS paper , where the camera poses for each frame are precomputed using an offline SFM method. Therefore, handling outlier gaussian s is crucial for 3DGS-based SLAM methods.

Overall, 3DGS based Dense Semantic SLAM can be summarized as facing two key challenges: 1) Providing robust semantic reconstruction results under inconsistent semantic features. 2) Incrementally building a map that can accurately distinguish well-optimized and low-quality regions, while effectively filtering out outliers to improve reconstruction quality.

This paper proposes NEDS-SLAM, with the following key contributions:

<sup>∗</sup> corresponding author

- We propose the Spatially Consistent Feature Fusion module (SCFF), which combines semantic features with appearance features. This module addresses the spatial inconsistency of semantic features and provides a more robust semantic SLAM solution.
- We embed semantic features into Gaussian parameters instead of using category labels. We also introduce a lightweight encoder-decoder to prevent memory issues from high-dimensional semantic feature embedding.
- We present the Virtual Camera View Pruning (VCVP) method. VCVP generates multiple virtual camera views to ensure consistency, identifying and removing unstable gaussians caused by occlusions, camera pose errors, and parameter optimization issues, leading to a more accurate 3D Gaussian field.

## II. RELATED WORK

#### *A. Traditional approaches to dense semantic SLAM*

Real-time dense semantic SLAM systems face the challenge of effectively fusing semantic information into underlying 3D geometric representations of the environment. Traditional approaches use voxels, point clouds, and signed distance fields to encode object labels [\[7\]](#page-7-6), [\[8\]](#page-7-7). However, voxel- and point cloud-based approaches struggle with reconstruction speed and high-fidelity model acquisition. Meanwhile, signed distance field representations incur high memory usage that does not scale well to large-scale environments. There remains a need for more efficient and expressive 3D semantic modeling techniques suitable for real-time dense SLAM.

## *B. NeRF based SLAM*

In recent years, Neural Radiance Fields (NeRF) have sparked significant interest in computer graphics, attracting attention for their high-fidelity novel view synthesis and lightweight scene representation [\[9\]](#page-7-8). This enthusiasm has quickly spread to the SLAM field, leading to the development of many innovative SLAM architectures [\[2\]](#page-7-1) [\[3\]](#page-7-2). Zhu et al. introduced SNI-SLAM [\[10\]](#page-7-9), which employs neural implicit representation and hierarchical semantic encoding for multi-level scene understanding, contributing a cross-attention mechanism for the collaborative integration of appearance, geometry, and semantic features. Due to the limitations of NeRF's volume rendering, NeRF-based dense semantic SLAM struggles to simultaneously model and optimize the semantic and RGB-geometry information of the environment [\[11\]](#page-7-10) [\[12\]](#page-7-11). Additionally, the efficiency of SLAM is constrained by the implicit representation of the map [\[13\]](#page-7-12).

#### *C. Gaussian Splatting based SLAM*

3DGS representations have emerged as a promising approach for 3D scene modelling using a set of 3D gaussians, each characterized by parameters such as position, anisotropic covariance, opacity, and color [\[14\]](#page-7-13). While existing 3DGSbased SLAM methods have primarily focused on RGB reconstruction, exploring end-to-end system architectures, optimization of gaussians parameters, and accurate camera pose tracking through differentiable rendering, less attention has been paid to semantic reconstruction [\[5\]](#page-7-4), [\[15\]](#page-7-14), [\[4\]](#page-7-3), [\[16\]](#page-7-15). The few semantic 3DGS-SLAM approaches proposed to date have simply encoded ground truth semantic color labels directly as a second color channel of the gaussians parameters [\[6\]](#page-7-5), without explicit modeling of semantic information or inference. There is clear potential for more sophisticated integration of semantics within the 3DGS-SLAM framework. The present work conducts a more in-depth exploration of dense semantic SLAM, aiming to simultaneously improve the robustness and reconstruction fidelity of 3DGS-based SLAM systems through more sophisticated modeling and inference of semantic information within the 3DGS representation.

#### III. METHODOLOGY

#### <span id="page-1-3"></span>*A. Scene Representation and Semantic embedding*

Each 3DGS utilized for representing three-dimensional scenes encompasses mean, covariance, and color information. In this paper, a simplified 3DGS representation of the scene is employed [\[5\]](#page-7-4), omitting the spherical harmonics functions used for color representation, while assuming gaussians to be isotropic as in Eq [1.](#page-1-0)

<span id="page-1-0"></span>
$$f^{gs}\left(\boldsymbol{x}\right) = o \exp\left(-\frac{\left\|\boldsymbol{x} - \boldsymbol{\mu}\right\|^2}{2r^2}\right) \tag{1}$$

Where µ ∈ R 3 represents the center position, r is the radius, and o ∈ [0, 1] represents the opacity. The rapid and differentiable rendering based on 3DGS serves as the core of mapping and tracking within 3DGS-based SLAM systems. This ability for fast rendering enables the system to directly compute the gradients of the underlying parameters based on the discrepancy between the rendered results and the actual data. Consequently, the gaussians parameters can be updated to achieve an accurate representation of the scene. The differentiable rendering process based on gaussians splatting comprises three steps: Frustum Culling, Splatting, and Rendering by Pixels [\[17\]](#page-7-16).

<span id="page-1-1"></span>
$$C(p) = \sum_{i \in N} c_i f_i^{gs}(p) \prod_{j=1}^{i-1} (1 - f_j^{gs}(p))$$
 (2)

After arranging a collection of 3D gaussians and camera pose, it is imperative to sort the gaussians in a front-toback manner. By employing alpha-compositing, the splatted 2D projection of each gaussian can be efficiently rendered in pixel space, ensuring the generation of RGB images in the desired order, as Eq [2.](#page-1-1) c<sup>i</sup> represents the color parameters of the gaussians, and f gs i (p) is computed as in Eq [1](#page-1-0) but with the 2D splatted µ and r. The rendering process is completed by multiplying the opacity of each gaussian with the color and accumulating the results. The depth map is rendered in a similar manner, as shown in Eq [3.](#page-1-2)

<span id="page-1-2"></span>
$$D(p) = \sum_{i \in N} d_i f_i^{gs}(p) \prod_{j=1}^{i-1} (1 - f_j^{gs}(p))$$
 (3)

The most notable distinction between semantic features and color and geometric features lies in their high-dimensional

![](_page_2_Figure_1.jpeg)

<span id="page-2-1"></span>Figure 1. Overview of the proposed NEDS-SLAM. Our method takes an RGB-D stream as input. RGB images are processed by the pretrained semantic feature extractor to get semantic features, while dense appearance features are obtained through the Spatial Feature Extractor model. The semantic and appearance features are fused to generate high-dimensional semantic features that are spatially consistent. These features are then processed by the encoder to generate low-dimensional features and embedded into the GS parameters. By employing Differentiable Rendering, real RGB images, depth images, and semantic masks predicted by a pre-trained segmentation head are utilized for Multi-Channel supervision. This approach enables the joint optimization of GS parameters. In the figure, M, C, and D represent the semantic segmentation mask, color, and depth information, respectively. NEDS-SLAM achieves high-fidelity map reconstructions while simultaneously accomplishing compact and dense pixel-level semantic reconstruction.

attributes. The semantic features do not refer to the per-pixel class labels generated by the segmentation head. Instead, it pertains to the high-dimensional semantic features extracted by the pre-trained model at each pixel. Taking DINO [18] as an example, the ViT-S model produces latent feature encodings of 384 dimensions, while the ViT-G model produces encodings of 1536 dimensions.

A simple way to combine 3DGS with semantic features is to add trainable feature vectors to each gaussian. These parameters can be learned during the differentiable rendering process, which allows end-to-end training. However, for dense semantic SLAM, adding a high dimensional semantic feature vector to each 3DGS is memory-inefficient. Inspired by LangSplat [19], we propose using a simple MLP as an encoder to compact semantic features into a low-dimensional vector. The compressed semantic features are then added to the 3D gaussians and can be rendered as in Eq. 4.

<span id="page-2-0"></span>
$$S(p) = \sum_{i \in N} f_i f_i^{gs}(p) \prod_{j=1}^{i-1} (1 - f_j^{gs}(p))$$
 (4)

#### B. Adaptive 3D Gaussian Expansion Mapping

1) Spatially Consistent Feature Fusion (SCFF): Pervious semantic SLAM approaches typically use pretrained segmentation models to compute pixel-level labels from each RGB frame, but these class labels lack environmental specificity. Pretrained models may produce inconsistent semantic estimates, where the same object is predicted with different semantic labels in images from different camera views.

To address this issue, SNI-SLAM [10] computes a fused feature by combining geometry, appearance, and semantic features. CoSSegGaussians [20] incorporates DINO [18] features with superior multi-view semantic scale consistency into the gaussians parameters. Subsequently, the semantic encoding

of each gaussians is fused with spatial coordinates to render semantic features, thereby enhancing robustness.

In this paper, we propose a simplified fusion mechanism. It combines the appearance features with the semantic features extracted from pretrained model. The resulting mixed feature, obtained through MLP encoder, is then embedded as the final semantic encoding in the 3DGS representations.

As shown in Fig 1, the pretrained semantic feature extractor extracts an  $H \times W \times D_f$  feature map  $F_{df}$  from an  $H \times W \times 3$  RGB frame. At the same time, the spatial feature extractor extracts  $H \times W \times D_s$  features  $F_{ds}$  from RGB data. After three layers of convolution, the feature channels of  $F_{df}$  are reduced to 256, 128, and 16, respectively. Similarly, the feature channels of  $F_{ds}$  are increased to 16 through one layer of CNN. After concatenation and the final convolution, we obtain the spatially consistent feature  $F_{scff}^{32}$  with 32 channels. Using the external parameters of the camera, we can convert an input frame of RGBD into a series of points in 3D space. Each point includes xyz coordinates, RGB information, and 32-channel SCFF features.

To reduce the number of 3D gaussian parameters, we need to use an information encoding method to compress  $F_{scff}^{32}$  to a lower dimension, such as using hash encoding [21], GPR [22], etc. In this paper, we use a simple MLP to compress  $F_{scff}^{32}$  to three dimensions, resulting in  $F_{scff}^{3}$ .

It is important to clarify that the semantic category labels are numerical IDs from a predefined category library (e.g., 0 represents a person), while the  $F_{scff}^3$  values range between 0 and 1. These semantic features can be decoded back into semantic category labels by a subsequent decoder.

We use the pre-trained DINO [18] model as a semantic feature extractor, obtaining features  $F_{df}$  with 384 channels ( $D_f=384$ ). We use DepthAnything [23] as the spatial feature extractor, resulting in  $D_s=1$ . Relative depth output from DepthAnything is used as the appearance feature because

changes in the camera viewpoint do not affect the relative position of surfaces on the object. The spatial consistency of appearance features helps SCFF achieve stable semantic feature estimation.

The relative depth between pixels can reflect the geometric structure of observed surfaces. The SCFF module dynamically adjusts the weights of semantic features according to the spatially consistent relationships. It thereby reduces the impact of segmentation errors on the spatial consistency of semantic features

2) Updating 3D Gaussians: During the mapping process, we assume that the camera pose for the current frame is known. We need to use the current keyframe's RGBD data to update the gaussians representation of the scene. Updating has two meanings: optimizing existing scene parameters and generating a new 3DGS distribution for the scene.

Following the processes used in Splatam [5] and GS-SLAM [15], we use Eq.5 to calculate the silhouette value per pixel. The silhouette images are rendered to determine the contribution of each gaussian to the map.

<span id="page-3-0"></span>
$$Sil(p) = \sum_{i \in N} f_i^{gs}(p) \prod_{j=1}^{i-1} (1 - f_j^{gs}(p))$$
 (5)

At the same time, the difference between the projected depth value and the ground truth value of pixels corresponding to newly added gaussian is checked when they are projected back onto the image plane.

<span id="page-3-1"></span>
$$M(p) = [Sil(p) < T_s] + [(D_{at}(p) - D(p)) < T_d]$$
 (6)

The densification mask  $M\left(p\right)$  is calculated according to Eq 6, where  $D\left(p\right)$  represents the depth value of pixel p.  $M\left(p\right)$  represents a Boolean mask for pixel p. The optimization of 3DGS and the addition of new gaussians will be confined to areas where the mask value is True, thereby avoiding the densification of gaussians in well-reconstructed areas. This differs from the approach in [14], which splits gaussians in over-reconstructed regions. Due to the high real-time requirements of SLAM systems, setting threshold parameters in  $M\left(p\right)$  allows the system to avoid the heavy computation associated with the gaussians densification method in [14].

After the process discussed in Section III-A, the scene representations contains three feature channels: spatial position, surface color, and potential semantics. The spatial position and surface color are directly obtained from the RGBD data stream. Meanwhile, the fusion of semantic encoding is supervised by the mask output from a pretrained segmentation model.

<span id="page-3-2"></span>
$$L_c = \lambda L_1 (I_r, I_{at}) + (1 - \lambda) [1 - ssim(I_r, I_{at})]$$
 (7)

The color loss  $L_c$  is represented as a weighted combination of SSIM [14] and L1 loss as in Eq 7.

<span id="page-3-3"></span>
$$L_d = \sum_{pix} \left| D_{pix}^{render} - D_{pix}^{gt} \right| \tag{8}$$

The depth loss  $L_d$  is calculated as in Eq 8. During the mapping stage, the multi-channel loss is as shown in Eq 9, where  $S_{render}$  represents the semantic labels after decoding

![](_page_3_Picture_14.jpeg)

Figure 2. The concept of virtual view pruning for identifying outlier gaussians. We analyze only the gaussians visible in the current ground-truth view (points A, B, C in the figure). Point A is not visible from either of the two virtual views, thus identified as an outlier gaussians, and its opacity is degraded during subsequent optimization. While the figure depicts two virtual views in a planar scenario, our approach creates four virtual cameras by rotating the camera pose from the focal point of each GT view frame along four directions: up, down, left, and right.

<span id="page-3-5"></span>the semantic features and  $S_{head}$  represents the class labels computed by the pretrained model. We use the cross-entropy loss  $L_{CE}$  to supervise the semantic channel.

<span id="page-3-4"></span>
$$L_{mapping} = \lambda_c L_c + \lambda_d L_d + \lambda_s L_{CE} \left( S_{render}, S_{head} \right) \tag{9}$$

In Eq 9,  $\lambda_d$ ,  $\lambda_s$ , and  $\lambda_c$  are predefined hyperparameters used to assign weighted values to the depth, semantic, and color channels respectively.

3) Vitrual Camera View Pruning 3D Gaussians (VCVP): The key aspects of GS-based SLAM are: 1) Distinguishing well-established areas from areas requiring further optimization, and 2) Identifying and removing outlier points. The former resolves where to add gaussians, and also plays a key role in camera tracking. Areas of low quality can severely affect the accuracy of pose tracking. The second key aspect resolves where to delete gaussians. Outlier points will cause holes and defects during image rendering, and these flaws can also affect the accuracy of camera tracking.

The distinction between well-optimized and areas with low quality is implemented through Eq 6. This section discusses issues related to gaussians pruning.

Multi-view consistency constraints have been proven effective in identifying geometrically unstable gaussians. Previous methods [4] check whether gaussians inserted within the latest three frames of a keyframe window are recorded by other keyframes, thereby determining outlier gaussians. This method improves mapping accuracy by using collaborative constraints among multiple keyframes, but it increases computational costs and reduces real-time performance. Drastic viewpoint changes during SLAM cause significant overlap variations between keyframes, leading to errors in outlier detection.

In contrast to this method, the VCVP method proposed in this paper does not perform comparison between keyframes. Instead, it compares the viewpoint between a real camera frame and the corresponding virtual accompanying camera frame, as depicted in Fig 2. The virtual cameras (VC) are created by rotating the real camera  $\pm \theta$  around the focal point:

![](_page_4_Picture_1.jpeg)

Figure 3. Rendered virtual camera views on the ScanNet dataset. The middle images provide a zoomed-in illustration of the effectiveness of Virtual Camera Pruning, where 'vcvp' denotes virtual camera view. Eliminating outlier gaussians not only improves rendering quality but also reduces the storage footprint of the map representation.

<span id="page-4-0"></span>V C<sup>1</sup> and V C<sup>2</sup> by rotating on the horizontal plane (xz plane), and V C<sup>3</sup> and V C<sup>4</sup> by rotating on the vertical plane (yz plane).

The points A and B represent outlier gaussians, while the GT view denotes the camera pose estimated within the RGBD stream. In the current keyframe, both A and B are visible. However, in the V C1, neither of these outlier points is visible, and in the V C2, only B is visible while A is not. The virtual camera operates alongside the real camera. If a gaussians is invisible in all virtual views but visible in the real view, it is then considered an outlier.

The virtual multi-view consistency check method takes advantage of the fast rendering capabilities of the Gaussian Splatting, enabling the marking of gaussians that significantly deviate from the object surface. The VCVP method eliminates the dependence on historical keyframes, allowing it to remain unaffected by drastic changes in camera views. This enables the identification of single-view outlier gaussians.

In subsequent optimization processes, the involvement of outlier gaussians in the scene is diminished by degrading their opacity. Consistent with [\[14\]](#page-7-13), gaussians with near-zero opacity or excessive radius are removed in the mapping process. As illustrated in Fig [3,](#page-4-0) we render virtual views and further optimize the 3D gaussians parameters only for keyframes. The specific approach for generating virtual views is not fixed. Although Gaussian splatting enables extremely fast virtual view synthesis (nearly 300 FPS), introducing too many viewpoints can compromise the system's real-time performance. We conducted detailed tests in Section [IV-C](#page-5-0) to evaluate how the generation and function of the virtual camera impact the performance of the SLAM system. We choose four virtual views along the up, down, left, and right directions, which achieves a desirable balance between effectiveness and efficiency.

*4) Camera tracking:* The camera tracking phase involves estimating the relative pose of the camera for each new frame, based on the already established map model. The camera pose for the new frame is initialized under the assumption of constant velocity, which includes both a constant linear and angular velocity.

![](_page_4_Figure_8.jpeg)

<span id="page-4-3"></span>Figure 4. The first row shows the RGB reconstruction results. The second row shows the semantic labels predicted directly on the current frame using M2F [\[24\]](#page-7-23). The third row shows the semantic reconstruction results using the SGS-SLAM [\[6\]](#page-7-5) method based on SplaTAM [\[5\]](#page-7-4). The fourth row shows the reconstruction results of our proposed model.

<span id="page-4-2"></span>Table I COMPARISON EXPERIMENTS WITH OTHER METHODS ON MAP RECONSTRUCTION AND LOCALIZATION ACCURACY

| Methods         | Depth L1[cm]↓ | LPIPS↓ | SSIM↑ | PSNR↑ | ATE RMSE[cm] ↓ |
|-----------------|---------------|--------|-------|-------|----------------|
| NICE-SLAM [3]   | 1.903         | 0.23   | 0.81  | 24.22 | 2.503          |
| Vox-Fusion [25] | 2.913         | 0.24   | 0.80  | 24.41 | 1.473          |
| Co-SLAM [26]    | 1.513         | 0.336  | 0.94  | 30.24 | 1.059          |
| ESLAM [27]      | 0.945         | 0.34   | 0.929 | 29.08 | 0.678          |
| SplaTAM [5]     | 0.49          | 0.10   | 0.97  | 34.11 | 0.36           |
| NEDS-SLAM(Ours) | 0.47          | 0.088  | 0.962 | 34.76 | 0.354          |

The camera pose is subsequently refined iteratively by minimizing the tracking loss between the ground truth of the color, depth, and semantic channels and the gaussian rendered results from the camera's perspective.

<span id="page-4-1"></span>
$$L_{\text{tracking}} = (\lambda_c L_c + \lambda_d L_d + \lambda_s L_{\text{CE}}(S_{\text{render}}, S_{\text{head}})) \cdot M \quad (10)$$

M in Eq [10](#page-4-1) is computed as Eq [6.](#page-3-1) Artifacts and flaws such as holes and spurious effects caused by outlier gaussians significantly impact the precision of camera tracking. Subsequent experiments demonstrate that the incorporation of semantic loss improve the tracking accuracy. This improvement is attributed to the enriched understanding of the geometric information of objects, facilitated by the integration of semantic features.

## IV. EXPERIMENT

#### <span id="page-4-4"></span>*A. Experimental Setup*

Dataset. We evaluate our method on both synthetic and realworld datasets with semantic maps. Following other nerf-based and gaussian-based SLAM methods, for the reconstruction quality, we evaluate quantitatively on 8 synthetic scenes from Replica [\[29\]](#page-7-27) and qualitatively on 6 scenes from ScanNet [\[30\]](#page-7-28).

Table II COMPARISON EXPERIMENT ON THE ATE RMSE METRIC

<span id="page-5-1"></span>

| Methods         | scene0000 | scene0169 | scene0181 | scene0207 | Avg.  |  |
|-----------------|-----------|-----------|-----------|-----------|-------|--|
| NICE-SLAM [3]   | 12.00     | 10.90     | 13.40     | 6.20      | 10.63 |  |
| Vox-Fusion [25] | 68.84     | 27.28     | 23.30     | 9.41      | 32.21 |  |
| Point-SLAM [28] | 10.24     | 22.16     | 14.77     | 9.54      | 14.18 |  |
| SplaTAM [5]     | 12.56     | 11.09     | 11.07     | 7.46      | 10.54 |  |
| NEDS-SLAM(Ours) | 12.34     | 11.21     | 10.35     | 6.56      | 10.12 |  |

# **PSNR: 28.41 PSNR: 31.71 splatam NEDS-SLAM (ours)**

<span id="page-5-2"></span>![](_page_5_Figure_5.jpeg)

struction quality in our study. These include the peak signal-tonoise ratio (PSNR), Depth-L1 (on 2D depth maps), Structural Similarity (SSIM [\[31\]](#page-7-30)), and Learned Perceptual Image Patch Similarity (LPIPS [\[32\]](#page-7-31)). Additionally, we assess the accuracy of camera pose estimation using the average absolute trajectory error (ATE RMSE [\[33\]](#page-7-32)). To evaluate the performance of semantic segmentation, we calculate the mIoU (mean Intersection over Union) score.

Baselines. We compare the tracking and mapping with stateof-the-art methods NICE-SLAM [\[3\]](#page-7-2), Co-SLAM [\[26\]](#page-7-25), ESLAM [\[27\]](#page-7-26), and SplaTAM [\[5\]](#page-7-4). For semantic segmentation accuracy, we compare with NIDS-SLAM [\[12\]](#page-7-11), DNS-SLAM [\[11\]](#page-7-10), and SNI-SLAM [\[10\]](#page-7-9).

Implementation Details. We conducted experiments using a single NVIDIA RTX 4090 and an Intel Xeon Platinum 8358P, validating on the REPLICA dataset with the mapping iteration set to 40, tracking iteration set to 60, and SCFF iteration set to 50. After obtaining 384 feature channels through the DINO model, we derived 64-dimensional fused features by applying 2D convolutions separately to the Spatial Features. Finally, we obtained three-dimensional features by passing them through an encoder and embedding them into the gaussians parameters. We use a learning rate of 0.005 and 0.001 respectively for all learnable parameters on Replica and ScanNet datasets. For camera poses, we only employ a learning rate of 0.0005 in tracking.

#### *B. Experiment result*

Quantitative measures of reconstruction quality using the Replica dataset are presented in Table [I.](#page-4-2) The experiments on

Table III COMPARISON EXPERIMENT ON THE MIOU METRIC

<span id="page-5-3"></span>

| Methods        | AVG.mIoU[%] ↑ | Room0 | Room1 | Office0 |
|----------------|---------------|-------|-------|---------|
| NIDS-SLAM [12] | 82.37         | 82.45 | 84.08 | 85.94   |
| DNS-SLAM [11]  | 84.77         | 88.32 | 84.90 | 84.66   |
| SNI-SLAM [10]  | 87.41         | 88.42 | 87.43 | 87.63   |
| Ours           | 90.78         | 90.73 | 91.20 | 90.42   |

the ScanNet dataset can be found in Table [II.](#page-5-1) The data shows that our method achieves the highest camera pose tracking accuracy. Our method demonstrates competitive performance when compared to other approaches. As shown in Fig [5,](#page-5-2) due to the VCVP method removing geometrically unstable gaussians,

our approach is able to preserve more details.

The NEDS-SLAM, built upon the foundation of 3DGS, achieves accurate camera localization and semantic reconstruction simultaneously. Table [III](#page-5-3) provides a comparison between our method and other neural Implicit approaches in terms of semantic reconstruction performance.

Due to the precise representation of object edges offered by the 3DGS, our methods bring about significant improvements in semantic reconstruction. Other methods have not considered the issue of spatially inconsistent semantic estimation by pretrained semantic segmentation models on consecutive RGBD frame inputs. Therefore, for the sake of fair performance comparison in Table [III,](#page-5-3) we used the ground truth per-pixel semantic class labels as input. More detailed experiments on the SCFF module are conducted in Table [V](#page-6-0) in Section [IV-C.](#page-5-0)

When testing the Mask2Former model on the replica room0 scene, as shown in Fig [4,](#page-4-3) there are noticeable inconsistencies in the predictions for the floor and chairs. This affects the semantic reconstruction quality. As shown in Fig [4,](#page-4-3) NEDS-SLAM effectively filters out the negative impact of spatial semantic inconsistencies, generating robust semantic estimates and providing more accurate semantic reconstruction.

#### <span id="page-5-0"></span>*C. Ablation Study*

## Effectiveness of VCVP Module.

The VCVP method involves two subproblems: (1) determining the number of virtual camera views to generate and how to generate them, and (2) deciding on which frame or frames to perform VCVP operation. The solutions to these subproblems will impact the computational costs of the VCVP modules. In Table [IV,](#page-6-1) the data in the third and fourth rows labeled 'A/B/C' indicates that we used three configurations for the calculations. Configuration A and B represent generating two virtual views in the horizontal and vertical directions, respectively. Configuration C represents generating four virtual views simultaneously in both horizontal and vertical directions.

The VCVP module significantly enhances scene modeling accuracy and camera pose tracking precision. Increasing the number of virtual camera views and their usage within the keyframes window can achieve the best camera localization accuracy, but this also increases computational overhead. In our most extreme test case, VCVP detection was performed on 10 keyframes during each mapping iteration, with four virtual

![](_page_6_Figure_1.jpeg)

<span id="page-6-3"></span>Figure 6. The validation results on the Scannet scene0000 00 dataset. The first row indicates the RGB reconstruction results of NEDS-SLAM, the second row indicates the semantic features predicted by M2F, the third row is the semantic reconstruction results without the Spatially Consistent Feature Fusion (SCFF) module, and the fourth row is the results with the SCFF module.

<span id="page-6-1"></span>Table IV ABLATION EXPERIMENTS ON THE VCVP MODULE CONDUCTED IN REPLICA ROOM0.

| Settings        | ATE<br>RMSE ↓  | AVG<br>SSIM ↑  | Scene<br>Embedding ↓ | Mapping<br>/iteration ↓ |
|-----------------|----------------|----------------|----------------------|-------------------------|
| Base1           | 0.42           | 0.90           | 100.16 MB            | 14 ms                   |
| Base + VCVP w5* | 0.30/0.34/0.28 | 0.91/0.93/0.96 | 90.45 MB             | 16/16/20 ms             |
| Base + VCVP w10 | 0.26/0.27/0.22 | 0.92/0.92/0.97 | 88.93 MB             | 18/18/26 ms             |
| Base + RCVP2    | 0.36           | 0.95           | 95.27 MB             | 20 ms                   |
| SplaTAM [5]     | 0.36           | 0.98           | 100.00 MB            | 24 ms                   |
| Co-SLAM [26]    | 0.97           | 0.91           | -                    | 13 ms                   |
| NICE-SLAM [3]   | 0.99           | 0.69           | 48.48 MB             | 66 ms                   |

<sup>1</sup> Base refers to the configuration without SCFF, without lightweight encoder, and without VCVP, implementing only the 3DGS dense SLAM functionality.

camera viewpoints rendered for each detection, resulting in nearly a 50% improvement in pose accuracy

We conducted another experiment comparing our method to the density control method (denote as DC method) from the original 3DGS paper, as in Table[.VII.](#page-6-2) In experiments on three scenes from the TUM RGBD dataset, the DC method achieved ATE RMSE values of 3.62, 1.41, and 6.63, which are higher than those of GS-SLAM, which also uses partial DC operations (3.3, 1.3, and 6.6 respectively). Our VCVP method demonstrated even higher performance.

## Effectiveness of SCFF Module.

Following SGS-SLAM, we directly incorporated semantic parameters into the 3D gaussians by calling a pre-trained M2F segmentation model [\[24\]](#page-7-23) on each RGB frame. As shown in

Table V ABLATION STUDY OF THE SCFF MODULE ON SCANNET DATASET.

<span id="page-6-0"></span>

| Settings                      | mIoU ↑ | Mapping<br>/iteration ↓ | Scene<br>Embedding ↓ |
|-------------------------------|--------|-------------------------|----------------------|
| Base S                        | 26.52% | 28 ms                   | 123.08 MB            |
| Base S + SCFF wo SFE          | 30.24% | 86 ms                   | 405.64 MB            |
| Base S + SCFF w SFE           | 42.18% | 86 ms                   | 410.38 MB            |
| Base S + SCFF w SFE + encoder | 40.81% | 35 ms                   | 141.93 MB            |

<span id="page-6-4"></span>Table VI RUNTIME PERFORMANCE COMPARISON OF NEDS-SLAM ON TWO DIFFERENT HARDWARE PLATFORMS.

| Hardware                 |                | # replica room0 | # TUM RGBD fr1/desk |                |  |
|--------------------------|----------------|-----------------|---------------------|----------------|--|
| Settings                 | Tracking/it ↓  | Mapping/it ↓    | Tracking/it ↓       | Mapping/it ↓   |  |
| Platform A<br>Platform B | 28 ms<br>42 ms | 35 ms<br>76 ms  | 26 ms<br>42 ms      | 34 ms<br>75 ms |  |

the third row in Fig [4,](#page-4-3) corresponding to the Base S settings in Table [V.](#page-6-0) SCFF wo SFE represents configurations includes the SCFF module, but does not use SFE. For the ScanNet scene0000 dataset, the M2F model achieved a semantic segmentation mIoU of 52.4. Using M2F for segmentation head gave an average mIoU of 26.52, serving as the baseline.

As can be seen in Fig [6,](#page-6-3) the semantic features calculated by the M2F model were inconsistent (such as the partitions and books on the table). After processing with the SCFF module, the inconsistencies were resolved and NEDS-SLAM output a more complete semantic reconstruction. The SCFF module filters out unstable semantic estimations between frames, resulting in more accurate semantic reconstruction. Our designed SCFF features a lightweight network structure, which does not significantly increase inference time. In fact, the time consumption in the SLAM process (Mapping/Iteration in the table) mainly arises from optimizing a large number of 3D gaussians. Therefore, our specially designed encoder compresses the semantic features and embeds them into the gaussian parameters, reducing the number of parameters and thereby increasing the mapping speed.

## Runtime Comparison.

As shown in the last column of Table [VI,](#page-6-4) our lightweight configuration of NEDS-SLAM achieves faster mapping speeds than SplaTAM while maintaining more accurate camera pose tracking precision. With higher configurations, NEDS-SLAM

<span id="page-6-2"></span>Table VII COMPARISON OF THE VCVP MODULE WITH THE ORIGINAL DENS ITY CONTROL METHOD ON TUM-RGBD DATASET.

| DATASETS                        | with VCVP            |                      | Original density control method as in [14] |                      |  |
|---------------------------------|----------------------|----------------------|--------------------------------------------|----------------------|--|
|                                 | ATE RMSE ↓           | AVG SSIM ↑           | ATE RMSE↓                                  | AVG SSIM ↑           |  |
| Fr1/desk1<br>Fr2/xyz<br>Fr3/off | 3.30<br>1.13<br>4.94 | 0.91<br>0.95<br>0.90 | 3.62<br>1.41<br>6.63                       | 0.93<br>0.95<br>0.92 |  |

Table VIII VERIFICATION OF THE EFFECTIVENESS OF THE SCFF MODULE

| Model Settings | M2F [24] | M2F+SCFF | MRCNN [34] | MRCNN+SCFF |
|----------------|----------|----------|------------|------------|
| AVG mIoU       | 25.89%   | 36.25%   | 24.34%     | 34.07%     |

<sup>\*</sup> VCVP w5(10) indicates selecting 5(10) frames from the current keyframes window for VCVP operations.

<sup>2</sup> RCVP involves using real camera views for consistency checks and removing outlier gaussians.

offers better performance, though the computation speed decreases. We ran NEDS-SLAM on different hardware platforms and datasets. Platform A is as in section [IV-A.](#page-4-4) Platform B consists of an Intel i9-13900K and a single NVIDIA RTX 4060Ti. The results show that both hardware platforms achieve similar camera pose tracking accuracy and reconstruction accuracy with NEDS-SLAM, but the model takes more time to run on Platform B compared to Platform A.

### V. CONCLUSION AND LIMITATIONS

The proposed NEDS-SLAM is an end-to-end semantic SLAM system based on 3DGS. By integrating a Spatially Consistent feature fusion model, NEDS-SLAM effectively addresses the challenges of robustly estimating semantic labels with pre-trained models, significantly enhancing semantic reconstruction performance. The Virtual Camera View Pruning method uses differentiable Gaussian splatting for quick and realistic novel view synthesis. It removes outlier gaussians during SLAM, significantly improving the reconstruction quality of neural radiance fields.

The experiment with public datasets confirmed NEDS-SLAM's effectiveness but revealed some shortcomings. The virtual camera view pruning method improves mapping speed by removing more gaussians. However, increasing the frequency of VCVP usage also raises computational load, indicating room for further optimization. Future plans include optimizing and incorporating semantic reconstruction for dynamic scenes.

## REFERENCES

- <span id="page-7-0"></span>[1] R. A. Newcombe, S. Izadi, O. Hilliges, D. Molyneaux, D. Kim, A. J. Davison, P. Kohi, J. Shotton, S. Hodges, and A. Fitzgibbon, "Kinectfusion: Real-time dense surface mapping and tracking," in *2011 10th IEEE international symposium on mixed and augmented reality*. Ieee, 2011, pp. 127–136.
- <span id="page-7-1"></span>[2] E. Sucar, S. Liu, J. Ortiz, and A. J. Davison, "imap: Implicit mapping and positioning in real-time," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2021, pp. 6229–6238.
- <span id="page-7-2"></span>[3] Z. Zhu, S. Peng, V. Larsson, W. Xu, H. Bao, Z. Cui, M. R. Oswald, and M. Pollefeys, "Nice-slam: Neural implicit scalable encoding for slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2022, pp. 12 786–12 796.
- <span id="page-7-3"></span>[4] H. Matsuki, R. Murai, P. H. J. Kelly, and A. J. Davison, "Gaussian Splatting SLAM," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024.
- <span id="page-7-4"></span>[5] N. Keetha, J. Karhade, K. M. Jatavallabhula, G. Yang, S. Scherer, D. Ramanan, and J. Luiten, "Splatam: Splat, track & map 3d gaussians for dense rgb-d slam," *arXiv preprint arXiv:2312.02126*, 2023.
- <span id="page-7-5"></span>[6] M. Li, S. Liu, and H. Zhou, "Sgs-slam: Semantic gaussian splatting for neural dense slam," *arXiv preprint arXiv:2402.03246*, 2024.
- <span id="page-7-6"></span>[7] A. Hermans, G. Floros, and B. Leibe, "Dense 3d semantic mapping of indoor scenes from rgb-d images," in *2014 IEEE International Conference on Robotics and Automation (ICRA)*. IEEE, 2014, pp. 2631–2638.
- <span id="page-7-7"></span>[8] G. Narita, T. Seno, T. Ishikawa, and Y. Kaji, "Panopticfusion: Online volumetric semantic mapping at the level of stuff and things," in *2019 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*. IEEE, 2019, pp. 4205–4212.
- <span id="page-7-8"></span>[9] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, "Nerf: Representing scenes as neural radiance fields for view synthesis," *Communications of the ACM*, vol. 65, no. 1, pp. 99–106, 2021.
- <span id="page-7-9"></span>[10] S. Zhu, G. Wang, H. Blum, J. Liu, L. Song, M. Pollefeys, and H. Wang, "Sni-slam: Semantic neural implicit slam," *arXiv preprint arXiv:2311.11016*, 2023.

- <span id="page-7-10"></span>[11] K. Li, M. Niemeyer, N. Navab, and F. Tombari, "Dns slam: Dense neural semantic-informed slam," *arXiv preprint arXiv:2312.00204*, 2023.
- <span id="page-7-11"></span>[12] Y. Haghighi, S. Kumar, J.-P. Thiran, and L. Van Gool, "Neural implicit dense semantic slam," *arXiv preprint arXiv:2304.14560*, 2023.
- <span id="page-7-12"></span>[13] F. Tosi, Y. Zhang, Z. Gong, E. Sandstr ¨om, S. Mattoccia, M. R. Oswald, and M. Poggi, "How nerfs and 3d gaussian splatting are reshaping slam: a survey," *arXiv preprint arXiv:2402.13255*, vol. 4, 2024.
- <span id="page-7-13"></span>[14] B. Kerbl, G. Kopanas, T. Leimk ¨uhler, and G. Drettakis, "3d gaussian splatting for real-time radiance field rendering," *ACM Transactions on Graphics*, vol. 42, no. 4, 2023.
- <span id="page-7-14"></span>[15] C. Yan, D. Qu, D. Wang, D. Xu, Z. Wang, B. Zhao, and X. Li, "Gsslam: Dense visual slam with 3d gaussian splatting," *arXiv preprint arXiv:2311.11700*, 2023.
- <span id="page-7-15"></span>[16] V. Yugay, Y. Li, T. Gevers, and M. R. Oswald, "Gaussian-slam: Photo-realistic dense slam with gaussian splatting," *arXiv preprint arXiv:2312.10070*, 2023.
- <span id="page-7-16"></span>[17] G. Chen and W. Wang, "A survey on 3d gaussian splatting," *arXiv preprint arXiv:2401.03890*, 2024.
- <span id="page-7-17"></span>[18] M. Oquab, T. Darcet, T. Moutakanni, H. V. Vo, M. Szafraniec, V. Khalidov, P. Fernandez, D. Haziza, F. Massa, A. El-Nouby, R. Howes, P.-Y. Huang, H. Xu, V. Sharma, S.-W. Li, W. Galuba, M. Rabbat, M. Assran, N. Ballas, G. Synnaeve, I. Misra, H. Jegou, J. Mairal, P. Labatut, A. Joulin, and P. Bojanowski, "Dinov2: Learning robust visual features without supervision," *arXiv:2304.07193*, 2023.
- <span id="page-7-18"></span>[19] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, "Langsplat: 3d language gaussian splatting," *arXiv preprint arXiv:2312.16084*, 2023.
- <span id="page-7-19"></span>[20] B. Dou, T. Zhang, Y. Ma, Z. Wang, and Z. Yuan, "Cosseggaussians: Compact and swift scene segmenting 3d gaussians," *arXiv preprint arXiv:2401.05925*, 2024.
- <span id="page-7-20"></span>[21] X. Zuo, P. Samangouei, Y. Zhou, Y. Di, and M. Li, "Fmgs: Foundation model embedded 3d gaussian splatting for holistic 3d scene understanding," *arXiv preprint arXiv:2401.01970*, 2024.
- <span id="page-7-21"></span>[22] Y. Yuan and A. N ¨uchter, "Uni-fusion: Universal continuous mapping," *IEEE Transactions on Robotics*, 2024.
- <span id="page-7-22"></span>[23] L. Yang, B. Kang, Z. Huang, X. Xu, J. Feng, and H. Zhao, "Depth anything: Unleashing the power of large-scale unlabeled data," *arXiv preprint arXiv:2401.10891*, 2024.
- <span id="page-7-23"></span>[24] B. Cheng, I. Misra, A. G. Schwing, A. Kirillov, and R. Girdhar, "Masked-attention mask transformer for universal image segmentation," 2022.
- <span id="page-7-24"></span>[25] X. Yang, H. Li, H. Zhai, Y. Ming, Y. Liu, and G. Zhang, "Voxfusion: Dense tracking and mapping with voxel-based neural implicit representation," in *2022 IEEE International Symposium on Mixed and Augmented Reality (ISMAR)*. IEEE, 2022, pp. 499–507.
- <span id="page-7-25"></span>[26] H. Wang, J. Wang, and L. Agapito, "Co-slam: Joint coordinate and sparse parametric encodings for neural real-time slam," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 13 293–13 302.
- <span id="page-7-26"></span>[27] M. M. Johari, C. Carta, and F. Fleuret, "Eslam: Efficient dense slam system based on hybrid representation of signed distance fields," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 17 408–17 419.
- <span id="page-7-29"></span>[28] E. Sandstr ¨om, Y. Li, L. Van Gool, and M. R. Oswald, "Point-slam: Dense neural point cloud-based slam," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 18 433–18 444.
- <span id="page-7-27"></span>[29] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma, *et al.*, "The replica dataset: A digital replica of indoor spaces," *arXiv preprint arXiv:1906.05797*, 2019.
- <span id="page-7-28"></span>[30] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, "Scannet: Richly-annotated 3d reconstructions of indoor scenes," in *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2017, pp. 5828–5839.
- <span id="page-7-30"></span>[31] Z. Wang, A. C. Bovik, H. R. Sheikh, and E. P. Simoncelli, "Image quality assessment: from error visibility to structural similarity," *IEEE transactions on image processing*, vol. 13, no. 4, pp. 600–612, 2004.
- <span id="page-7-31"></span>[32] R. Zhang, P. Isola, A. A. Efros, E. Shechtman, and O. Wang, "The unreasonable effectiveness of deep features as a perceptual metric," in *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2018, pp. 586–595.
- <span id="page-7-32"></span>[33] J. Sturm, N. Engelhard, F. Endres, W. Burgard, and D. Cremers, "A benchmark for the evaluation of rgb-d slam systems," in *2012 IEEE/RSJ international conference on intelligent robots and systems*. IEEE, 2012, pp. 573–580.
- <span id="page-7-33"></span>[34] W. Abdulla, "Mask r-cnn for object detection and instance segmentation on keras and tensorflow," [https://github.com/matterport/Mask](https://github.com/matterport/Mask_RCNN) RCNN, 2017.