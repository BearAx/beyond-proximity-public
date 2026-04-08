# Semantic Gaussians: Open-Vocabulary Scene Understanding with 3D Gaussian Splatting

Jun Guo<sup>∗</sup> , Xiaojian Ma<sup>∗</sup> , Yue Fan, Huaping Liu† ,*Senior Member, IEEE*, Qing Li†

*Abstract*—Open-vocabulary 3D scene understanding presents a significant challenge in computer vision, with wide-ranging applications in embodied agents and augmented reality systems. Existing methods adopt neurel rendering methods as 3D representations and jointly optimize color and semantic features to achieve rendering and scene understanding simultaneously. In this paper, we introduce Semantic Gaussians, a novel openvocabulary scene understanding approach based on 3D Gaussian Splatting. Our key idea is to distill knowledge from 2D pretrained models to 3D Gaussians. Unlike existing methods, we design a versatile projection approach that maps various 2D semantic features from pre-trained image encoders into a novel semantic component of 3D Gaussians, which is based on spatial relationship and need no additional training. We further build a 3D semantic network that directly predicts the semantic component from raw 3D Gaussians for fast inference. The quantitative results on ScanNet segmentation and LERF object localization demonstates the superior performance of our method. Additionally, we explore several applications of Semantic Gaussians including object part segmentation, instance segmentation, scene editing, and spatiotemporal segmentation with better qualitative results over 2D and 3D baselines, highlighting its versatility and effectiveness on supporting diverse downstream tasks.

*Index Terms*—open-vocabulary scene understanding, 3D Gaussian Splatting.

## I. INTRODUCTION

Open-vocabulary 3D scene understanding is a crucial task in computer vision. Given a 3D scene, the goal is to comprehend and interpret 3D scenes with free-form natural language, *i.e*., without being limited to a predefined set of object categories. Allowing open-vocabulary scene queries enables machines to interact more effectively with the environment, facilitating tasks like object recognition, semantic scene reconstruction, and navigation in complex and diverse surroundings. Openvocabulary 3D scene understanding has significant implications in various real-world applications such as robotics and augmented reality.

Various methods have been proposed to achieve openvocabulary 3D scene understanding, relying on different 3D scene representations such as multi-view RGB images [\[1\]](#page-10-0), point clouds [\[2\]](#page-10-1), [\[3\]](#page-10-2), and Neural Radiance Fields (NeRFs) [\[4\]](#page-10-3), [\[5\]](#page-10-4). Approaches based on these representations have their pros and cons: Multi-view images are the most straightforward representation of 3D scenes, but allowing open-vocabulary understanding usually involves 2D vision-language models [\[6\]](#page-10-5), which could struggle with consistency across different views,

This paper was produced by BIGAI and Tsinghua University. They are in Beijing, China.

likely due to a lack of visual geometric knowledge; Point clouds are popular and well-studied, but the inherent sparsity nature of point clouds limits the application of openvocabulary scene understanding upon them [\[2\]](#page-10-1), *e.g*., it is challenging to obtain a dense prediction on a 2D view; injecting open-vocabulary semantics to NeRFs could enjoy both high 2D rendering quality and dense free-form visual recognition [\[5\]](#page-10-4), but the implicit design requires open-vocabulary recognition training for every new scene, and the rendering speed becomes a bottleneck to achieve real-time high-quality scene understanding.

1

A recent alternative scene representation is 3D Gaussian Splatting (3DGS) proposed by Kerbl *et al*. [\[7\]](#page-10-6). It utilizes 3D Gaussian points with color, opacity, and covariance matrix to represent the 3D scene, which can be learned from multi-view RGB images via gradient descent training. It attains the NeRFlevel view rendering quality while preserving the explicit point-based characteristics similar to point clouds, making it suitable for open-vocabulary 3D scene understanding.

A main branch of previous approaches [\[4\]](#page-10-3), [\[5\]](#page-10-4), [\[8\]](#page-10-7)–[\[16\]](#page-10-8) is to adopt neural rendering methods like NeRF or 3DGS as the 3D representations, and jointly optimizing the color components and the semantic features, to achieve high-quality rendering and 3D scene understanding from arbitrary 2D views. The semantic knowledge is usually distilled from open-vocabulary 2D foundation models, such as CLIP [\[17\]](#page-10-9) or LSeg [\[18\]](#page-10-10), whose outputs predicted on training views serve as weak supervision during optimization.

In this work, we propose Semantic Gaussians, a novel approach to open-vocabulary 3D scene understanding building upon the benefits of 3D Gaussian Splatting. The core idea of Semantic Gaussians is to distill the knowledge from pretrained 2D encoders into 3D Gaussians, thereby assigning a semantic component to each Gaussian point. To achieve this, we establish correspondence between 2D pixels and 3D Gaussian points and propose a versatile projection framework to map the semantic features of 2D pixels onto each 3D Gaussian point. Our framework is rather flexible and can leverage arbitrary pre-trained 2D models, such as OpenSeg [\[19\]](#page-10-11), CLIP [\[17\]](#page-10-9), VLPart [\[20\]](#page-10-12), *etc*., to generate pixel-wise semantic features on 2D RGB images. Compared to previous approachs, our method injects semantic components into 3D Gaussians *without additional training*, allowing for effective open-vocabulary scene queries.

In addition to projection, we further introduce a 3D semantic network that directly predicts open-vocabulary semantic components out of raw 3D Gaussians. Specifically, we employ MinkowskiNet [\[21\]](#page-10-13), a 3D sparse convolution

<sup>\*</sup> Equal contribution.

<sup>†</sup> Corresponding author.

![](_page_1_Figure_1.jpeg)

Fig. 1. Overview of our Semantic Gaussians. We inject semantic features into off-the-shelf 3D Gaussian Splatting by either projecting semantic features from pre-trained 2D encoders or directly predicting pointwise embeddings by a 3D semantic network (or fusing these two). The newly added semantic components of 3D Gaussians open up diverse applications centered around open-vocabulary scene understanding.

network to process 3D Gaussians. The 3D convolution network takes raw RGB Gaussians as input and is supervised by the semantic components of Gaussians obtained from the aforementioned projection method. As a result, we may simply run this network to obtain the semantic components, enabling faster inference. This network leverages geometric attributes to understand unseen scenes, boosting the generalizability and robustness of our method beyond 2D projection. Note that the prediction of the 3D semantic network can be combined with the projected features to further improve the quality of semantic components in Gaussians and open-vocabulary scene understanding performances.

We conduct experiments on the ScanNet semantic segmentation benchmark [22] and LERF localization [5], and prove our efficiency compared to 2D pre-trained models. Besides segmentation and localization, we also explore diverse applications of Semantic Gaussians, including 3D part segmentation on the MVImgNet object dataset [23], instance segmentation and scene editing in multi-object scenes, and spatiotemporal tracking on 4D dynamic Gaussians [24].

In summary, our contributions are three-fold:

- We introduce Semantic Gaussians, a novel approach to open-vocabulary 3D scene understanding by bringing a novel semantic component to 3D Gaussian Splatting.
- 2) We propose a versatile semantic feature projection framework to map various pre-trained 2D features to 3D Gaussian points, and introduce a 3D semantic network to further allow direct prediction of these semantic components from raw 3D Gaussians;

3) We conduct experiments on the ScanNet and LERF localization datasets to demonstrate the effectiveness of our method on open-vocabulary scene understanding and explore various applications including object part segmentation, instance segmentation, scene editing, and spatiotemporal tracking.

#### II. RELATED WORK

### A. 3D Scene Representation

Modeling and representing 3D scenes are crucial initial steps in understanding such environments. Before the advent of deep learning, common methods involved simplifying scenes into combinations of basic elements. Classic approaches include point clouds, meshes, and voxels. Point clouds represent scenes as collections of points, where each point's XYZ coordinates together form the scene's geometric shape. Enhancing point clouds with RGB values, semantic labels, and other data enriches their ability to represent scenes. Meshes depict 3D scene surfaces using collections of polygons, with triangular meshes being the most common, representing surfaces as interconnected triangles. By recording the vertices and adjacency relationships of each triangle, 3D scenes can be effectively represented. Voxels discretize continuous 3D space into cubic units, extending the concept of pixels from 2D to 3D. Although these traditional methods have seen success, their limitations are increasingly apparent in today's pursuit of realistic reconstruction and rendering.

On the other hand, implicit neural representations, represented by Neural Radiance Fields (NeRF), have made re-

markable strides in various 3D computer vision tasks. NeRF was initially proposed by Mildenhall *et al*. [\[25\]](#page-10-17) to address the problem of novel view synthesis. By extracting shape and color information from images captured from multiple viewpoints and learning a continuous 3D radiance field via neural networks, NeRF achieves photorealistic rendering of 3D scenes from arbitrary viewpoints and distances. Succeeding works demonstrate the capability of NeRF in 3D scene representation. Semantic-NeRF [\[26\]](#page-10-18) explored encoding semantics into a NeRF to achieve 3D scene understanding. EditNeRF [\[27\]](#page-10-19) defines a conditional NeRF where 3D objects are conditioned on shape and appearance codes to achieve scene editing. Some works [\[28\]](#page-10-20), [\[29\]](#page-10-21) jointly predict a canonical space and a temporal deformation field to achieve dynamic scene reconstruction.

Recently, Kerbl *et al*. [\[7\]](#page-10-6) have proposed a new novel view synthesis method called 3D Gaussian Splatting, which represents the 3D scene with a set of 3D Gaussians. This method has demonstrated real-time rendering capabilities at 1080p resolution, achieving a remarkable 60 frames per second while maintaining state-of-the-art visual quality. The innovation behind 3D Gaussian Splatting lies in its incorporation of point-based α-blending and a differentiable tile rasterizer, enabling efficient rendering. Though it obtains a dense set of Gaussians via optimization, all parameters in these 3D Gaussians are explicit and editable. The speed enhancement and explicit parameterization position 3D Gaussian Splatting as a highly promising representation method. Building upon its success in novel view synthesis, some studies [\[24\]](#page-10-16), [\[30\]](#page-10-22)–[\[34\]](#page-10-23) have extended 3DGS to dynamic scenes. For example, Luiten *et al*. [\[24\]](#page-10-16) extended the concept to Dynamic 3D Gaussians, explicitly modeling 3D Gaussians at different time steps to accommodate 4D dynamic scenes. Furthermore, many recent works [\[33\]](#page-10-24)–[\[39\]](#page-10-25) leverage 3D Gaussian Splatting to achieve high-quality text-to-3D or image-to-3D generation. In this study, we propose an open-vocabulary 3D scene understanding method, leveraging the advantages offered by 3D Gaussian Splatting.

#### *B. Open-Vocabulary Scene Understanding*

*1) Scene understanding from 2D:* Encouraged by the availability of adequate text-image datasets and the advancement in vision language models, the field of 2D open-vocabulary scene understanding has made significant progress in recent years. Prevailing approaches [\[18\]](#page-10-10), [\[40\]](#page-10-26), [\[41\]](#page-10-27) distill knowledge from large-scale pre-trained foundation models (*e.g*., CLIP [\[17\]](#page-10-9)) to achieve zero-shot understanding, including recognizing longtail objects and understanding synonymous labels. However, these methods are limited to small partial scenes represented by a single 2D image. When it comes to 3D scenes, the prediction result of these 2D models can hardly remain consistent between different angles of view. In contrast, our work relies on these 2D pre-trained models to achieve 3D scene understanding, segmenting, and understanding the scene from a panoptic perspective. Moreover, the proposed 3D network can perform 3D-only scene understanding in the absence of 2D pre-trained models and images.

*2) Scene understanding from 3D:* Open-vocabulary 3D scene understanding has been a long-standing challenge in computer vision. Some point-cloud-based methods [\[2\]](#page-10-1), [\[42\]](#page-10-28)– [\[44\]](#page-11-0) encode the semantic features from 2D pre-trained models into 3D scene points to achieve open-vocabulary 3D scene understanding. To achieve high-quality rendering and scene understanding simultaneously, feature field distillation in NeRF has been well explored. Early works such as Semantic-NeRF [\[26\]](#page-10-18), Panoptic Lifting [\[45\]](#page-11-1) and Contrastive Lift [\[46\]](#page-11-2) embed semantic labels into NeRF, resulting in precise 3D segmentation maps. Encouraged by this idea, another branch of methods [\[4\]](#page-10-3), [\[5\]](#page-10-4), [\[8\]](#page-10-7)–[\[11\]](#page-10-29) integrate semantic embeddings from pre-trained models such as LSeg [\[18\]](#page-10-10), CLIP or DINO [\[47\]](#page-11-3) into NeRFs, achieving open-vocabulary 3D scene understanding. Recently, some works [\[12\]](#page-10-30)–[\[16\]](#page-10-8) have made efforts to transfer those NeRF-based methods to 3DGS, obtaining 3DGS with semantic features via optimization. Our work shares a similar idea with those methods, while the Semantic Gaussians requires no extra training for Gaussians. The explicit nature of 3D Gaussian Splatting enables Semantic Gaussians to achieve versatile projection from 2D semantic maps into 3D Gaussian points.

#### III. SEMANTIC GAUSSIANS

In this section, we illustrate the framework of our Semantic Gaussians. Fig. [2](#page-3-0) depicts the overall framework of our method. Semantic Gaussians starts from a group of 3D Gaussians (Sec. [III-A\)](#page-2-0), performing scene understanding on it through 2D versatile projection and 3D semantic network processing. We first introduce our versatile projection method that projects 2D semantic embeddings from various pre-trained visionlanguage models into 3D Gaussian points (Sec. [III-B\)](#page-3-1). We then depict the 3D semantic network that learns from the projected features and predicts the semantics of 3D Gaussians in unseen scenes (Sec. [III-C\)](#page-4-0). At last, we describe the feature ensemble process and use the prediction result to support various applications (Sec. [III-D\)](#page-4-1).

## <span id="page-2-0"></span>*A. 3D Gaussian Splatting*

To achieve general 3D open-vocabulary scene understanding, we employ 3D Gaussian Splatting [\[7\]](#page-10-6) as the representation of 3D scenes. 3DGS can render images from arbitrary viewpoints in a differentiable manner, thus effectively leveraging the knowledge of various 2D foundation models. Specifically, we achieve scene understanding by rendering 2D semantic images from specified viewpoints with 3DGS.

3DGS consists of a set of learnable 3D Gaussian points, where each point has a 3D coordinate µ representing its position, a covariance matrix Σ representing its shape, spherical harmonic parameters c representing its color, and an opacity value α representing its transparency. 3DGS can be constructed from multi-view images and can utilize information from Structure-from-Motion (SfM) point clouds [\[48\]](#page-11-4) for initialization, thereby achieving better rendering quality and geometric structure.

![](_page_3_Figure_1.jpeg)

<span id="page-3-0"></span>Fig. 2. An illustration of the pipeline of Semantic Gaussians. *Upper left:* our projection framework maps various pre-trained 2D features to the semantic component  $s^{2D}$  of 3D Gaussians; *Bottom left:* we additionally introduce a 3D semantic network that directly predicts the semantic components  $s^{3D}$  out of raw 3D Gaussians. It is supervised by the projected  $s^{2D}$ ; *Right:* given an open-vocabulary text query, we compare its embedding against the semantic components  $(s^{2D}, s^{3D}, or$  their fusion) of 3D Gaussians. The matched Gaussians will be splatted to render the 2D mask corresponding to the query.

3DGS uses point-based  $\alpha$ -blending to compute pixel values on 2D images. The value of each pixel C is given by volumetric rendering along a ray:

$$C = \sum_{i \in \mathcal{N}} c_i \alpha_i T_i \text{ with } T_i = \prod_{j=1}^{i-1} (1 - \alpha_j), \tag{1}$$

where  $\mathcal{N}$  is the set of sorted Gaussians in front-to-back depth order overlapping with the given pixel.  $\alpha_i$  is the opacity of point i, and  $c_i$  is the color of point i, which is calculated by spherical harmonics.

To project 3D Gaussians onto a certain 2D plane, Zwicker et al. proposed a splatting method to calculate the covariance matrix  $\Sigma'$  from the camera's viewpoint. Given the world-to-camera transformation matrix W, the covariance matrix in camera coordinates is given as follows:

$$\Sigma' = JW\Sigma W^T J^T, \tag{2}$$

where J is the Jacobian of the affine approximation of the projective transformation. If we skip the third row and column of  $\Sigma'$ , we can obtain the 2D variance matrix. To assure the positive semi-definite, the covariance matrix  $\Sigma$  is decomposed into rotation matrix R and scaling matrix S, which can be represented as follows:

$$\Sigma = RSS^T R^T. \tag{3}$$

3DGS can be regarded as a special point cloud with additional features, thus sharing some properties of point clouds. An intuitive idea is to project the semantic information obtained from 2D foundation models onto the corresponding Gaussian points based on spatial relationships, rather than through differentiable rasterization and rendering. When rendering semantic maps, it is sufficient to consider the correspondence of geometric positions without accounting for complex lighting conditions. Based on this idea, we propose Semantic Gaussians to achieve versatile scene understanding.

#### <span id="page-3-1"></span>B. 2D Versatile Projection

The first contribution of our approach is a versatile feature projection method. We extract pixel-level semantic maps for RGB images from a 2D pre-trained model and project them into 3D Gaussians of a scene.

- 1) Semantic Map Extraction: Our method starts from offthe-shelf 3D Gaussians G of a certain scene. We can use ground-truth RGB images that are used to train 3D Gaussians or render RGB frames via the 3D Gaussians. Owing to the photorealistic rendering performance of 3D Gaussian Splatting, Semantic Gaussians can run without 2D groundtruth images. Given RGB images I with a shape of  $H \times W$ , the aim of Semantic Gaussians is to get pixel-level semantic maps denoted by  $s \in \mathbb{R}^{H \times W \times C}$  from an arbitrary 2D vision-language model  $\mathcal{E}^{2D}$ . The most straightforward avenue to obtain per-pixel semantic maps is utilizing pixel-level segmentation models such as OpenSeg. However, leveraging other encoders, e.g. VLPart [20] could help with object parts semantics (not covered by OpenSeg). Moreover, features from different types of models can be integrated as an ensemble to produce more accurate results. Therefore, our versatile projection method should be able to reconcile various visual features.
- 2) Unifying Various 2D Features with SAM: Accommodating a variety of 2D pre-trained features is **non-trivial** as they can be pixel-level segmentation network (e.g., OpenSeg [19], LSeg [18]), instance-level recognition network (e.g., GroundingDINO [49], VLPart [20]), or image-level classification network (e.g., CLIP [17]). Additionally, Semantic Gaussians are able to utilizes Segment Anything (SAM) [50] to produce fine segmentation maps for each model. For pixel-level models, SAM can refine the segmentation boundary. Given an RGB image I, we use everything prompt in SAM to generate N binary masks  $\mathbf{M}_1, \dots, \mathbf{M}_N$ . We calculate the average pooling of embeddings in each mask  $\mathbf{M}_i$ , and assign it as the embedding of all pixels in this mask:  $s[\mathbf{M}_i] = AvgPool(s[\mathbf{M}_i])$ .

For instance-level models, we use SAM as the postprocessing module to get fine masks. Similar to Grounded-SAM [\[51\]](#page-11-7), we use the prediction result from the pre-trained model as the box prompt of SAM. After getting the binary mask, we assign the CLIP embedding of this instance to all the pixels within the instance region. For image-level models, SAM can be a preprocessing module to get region proposals. We use the "everything" prompt in SAM to get various proposed regions. Each region is padded, cropped, and resized to 224×224, and fed into the image-level model to get semantic embeddings. Similarly, the semantic embeddings are assigned to all pixels within each proposed region.

*3) 2D-3D Projection and Fusion:* After acquiring per-pixel semantic maps, Semantic Gaussians projects them into 3D Gaussians to obtain the semantic components. For each pixel u = (u, v) in a semantic mapping s, Semantic Gaussians tries to find if there are corresponding 3D Gaussian points p = (x, y, z) in the space. This can be achieved when the camera intrinsic matrix K and world-to-camera extrinsic matrix E are provided. Under the pinhole camera model, the projection can be formulated as u˜ = K · E · p˜, where u˜ and p˜ are the homogeneous coordinates of u and p. After this projection, every pixel u will correspond to a beam of ray in the 3D space. As we only expect to project 2D semantics to the surface points in 3D space, we perform depth rendering of 3D Gaussians to get the depth map of the 3D scene. During splatting and volume rendering, the opacity is accumulated from near to far. Therefore, we set an opacity threshold αd, and when the opacity surpasses αd, the ray of view is occluded by some opaque objects, where we can record the depth. Note that we do not need ground-truth depth from datasets.

When 2D pixels and 3D Gaussian points are paired, assuming that a certain Gaussian point p in 3D spaces has a group of 2D semantics {s1, · · · , sK} from K different views, these semantics can be fused by average pooling: s 2D <sup>p</sup> = AvgP ool(s1, · · · , sK). By repeating this process for all 3D Gaussian points, we can construct a group of semantic Gaussians for a 3D scene.

## <span id="page-4-0"></span>*C. 3D Semantic Network*

In addition to projecting 2D pre-trained features onto 3D Gaussians, we alternatively explore a more direct approach – predicting the semantic components from the raw 3D Gaussians. In this section, we build a 3D semantic network f 3D to do exactly that. Specifically, given the input 3D Gaussians G, our 3D network f 3D predict the point-wise semantic component s 3D, which can be formulated as Eqn. [4:](#page-4-2)

<span id="page-4-2"></span>
$$s^{3D} = f^{3D}(\mathbf{G}). \tag{4}$$

We use fused features from Sec. [III-B](#page-3-1) (denoted by s 2D) to supervise the 3D model. The loss function is the cosine similarity loss:

$$\mathcal{L} = 1 - \cos(s^{3D}, s^{2D}).$$
 (5)

We use MinkowskiNet [\[21\]](#page-10-13) as the backbone of our 3D model. MinkowskiNet is a 3D sparse convolution network designed for point clouds. Due to the similarity between 3D point clouds and 3D Gaussians, it can be utilized to process 3D Gaussians. Opacities, colors, and covariance matrixes are set as input features of our 3D model, and the output is the semantic embeddings s 3D of every Gaussian point.

Though the supervised target entirely comes from pretrained 2D encoders, the 3D model recognizes the scene by processing 3D geometric information rather than multiple 2D views, making the result more consistent. Experiments in Sec. [IV-B1](#page-5-0) show that the 3D prediction s 3D can complement 2D projection features s 2D. Also, the inference speed of our 3D semantic model is much faster than 2D projection.

## <span id="page-4-1"></span>*D. Inference*

After obtaining the semantic components of 3D Gaussians, we can perform language-driven open-vocabulary scene understanding. In this section, we will detail the inference process. Given a free-form language query, we use the CLIP text encoder to encode the prompts into text embedding t. We calculate the cosine similarity between the text embedding and the semantic component of every 3D Gaussian point and the matched Gaussians will be viewed as corresponding to the query. Take semantic segmentation and part segmentation as an example, labels of N semantic classes are encoded as t1, · · · , t<sup>N</sup> . We calculate the cosine similarity between these text embeddings and the semantic embedding of 3D Gaussians:

$$c_n^{\text{2D}} = 1 - \cos(s^{\text{2D}}, \mathbf{t}_n), c_n^{\text{3D}} = 1 - \cos(s^{\text{3D}}, \mathbf{t}_n)$$
 (6)

When 2D and 3D semantic components s 2D and s 3D both exists, we choose the larger value in c 2D n and c 3D n as the cosine similarity of the class tn. The similarities {c1, · · · , cn} after the softmax function can be the confidence score of each class. To get a 2D semantic segmentation map, the confidence scores are splatted onto 2D views, which is similar to RGB splatting.

## IV. EXPERIMENTS

In this section, we conduct various experiments to demonstrate the effectiveness of Semantic Gaussians on openvocabulary 3D scene understanding and other applications. We first evaluate and compare our method on the ScanNet 2D semantic segmentation benchmark which is constructed on 3D scenes. Then, we exhibit the 3D object localization results of Semantic Gaussians on LERF dataset. Next, we exhibit qualitative results on some applications, including part segmentation, spatiotemporal tracking, and language-guided editing. We also provide ablation study results.

#### *A. Experimental Setup*

*1) Datasets:* For comparisons on scene-level semantic segmentation, we select ScanNet [\[22\]](#page-10-14) dataset as our 2D segmentation benchmark. ScanNet is a large-scale segmentation benchmark of indoor scenes, with calibrated RGBD trajectories, 3D point clouds, and ground-truth semantic label maps. We train 3D RGB Gaussians for all 1,201 scenes. We train our 3D semantic network on ScanNet train set and evaluate

![](_page_5_Figure_1.jpeg)

<span id="page-5-1"></span>Fig. 3. Visualization of scene-level semantic segmentation performance for open-vocabulary 3D scene understanding methods on ScanNet dataset.

our performance on 12 scenes [\[45\]](#page-11-1) from the validation set. To compare with closed-set methods, we follow the setting of [\[45\]](#page-11-1) which maps ScanNet-20 classes to 21 classes from COCO dataset.

For 3D object localization tasks, we choose LERF [\[5\]](#page-10-4) dataset as our benchmark. LERF dataset provide several 3D scenes containing long-tail objects and multi-scale semantics. The dataset is captured by iPhone App Polycam to get multiview images and SfM points. In our experiments, we follow the setting of [\[12\]](#page-10-30) to evaluate the localization accuracy on 4 different scenes.

For qualitative evaluations, we choose MVImgNet [\[23\]](#page-10-15) dataset as our part segmentation dataset, and CMU Panoptic [\[52\]](#page-11-8) dataset as our spatiotemporal tracking dataset. MVImgNet is a multi-view single-object dataset containing 238 classes of objects with camera parameters and sparse point clouds. CMU Panoptic dataset is a large-scale dataset for multi-people engaging in social activities. For language-guided editing, we choose some scenes in the Mip-NeRF 360 [\[53\]](#page-11-9) dataset to show our performance.

*2) Implementation Details:* All our experiments are trained on a NVIDIA RTX 4090 GPU. We train 10000 iterations for RGB Gaussians and 100 epochs for 3D semantic network. For scene-level semantic segmentation experiments, We apply LSeg to generate pixel-level open-vocabulary semantic features for 2D projection. As for 3D semantic network, we use MinkowskiNet34A [\[21\]](#page-10-13) as our backbone. For 3D object localization tasks, we both apply CLIP with SAM and LSeg as our 2D pretrained model.

For part segmentation and spatiotemporal tracking, we use VLPart as our projection model. To evaluate our Semantic Gaussians on 4D Gaussians, we follow the work of Dynamic 3D Gaussians [\[24\]](#page-10-16) to obtain dynamic Gaussians with temporal information.

#### *B. Quantitative Results*

<span id="page-5-0"></span>*1) Open-Vocabulary Semantic Segmentation:* We first evaluate our approach on the scene-level semantic segmentation task. We compare our method with several methods, including closed-set and open-vocabulary segmentation methods. We choose both 2D segmentation models and 3D segmentation

![](_page_6_Figure_1.jpeg)

<span id="page-6-2"></span>Fig. 4. Qualitative comparisons of different methods on the MVImgNet part segmentation task. We choose 6 classes of objects with 3, 4 and 5 parts to show the part segmentation performance.

<span id="page-6-0"></span>TABLE I 2D SEMANTIC SEGMENTATION RESULTS ON 12 SCENES IN SCANNET VALIDATION SET. WE REPORT THE MEAN IOU AND THE MEAN ACCURACY ON ALL CLASSES.

| Method                  | Backbone     | mIoU | mAcc |
|-------------------------|--------------|------|------|
| closed-set methods      |              |      |      |
| Mask2Former [54]        | ViT          | 46.7 | -    |
| DM-NeRF [55]            | NeRF         | 49.5 | -    |
| SemanticNeRF [26]       | NeRF         | 59.2 | -    |
| Panoptic Lifting [45]   | NeRF         | 65.2 | -    |
| open-vocabulary methods |              |      |      |
| OpenSeg [19]            | EfficientNet | 53.4 | 75.1 |
| LSeg [18]               | ViT          | 56.1 | 74.5 |
| LERF [5]                | NeRF+CLIP    | 31.2 | 61.7 |
| PVLFF [56]              | NeRF+LSeg    | 52.9 | 67.0 |
| LangSplat [12]          | 3DGS+CLIP    | 24.7 | 42.0 |
| Feature3DGS [13]        | 3DGS+LSeg    | 59.2 | 75.1 |
| Ours 2D                 | 3DGS+LSeg    | 61.0 | 76.6 |
| Ours 3D                 | 3DGS+LSeg    | 59.7 | 74.7 |
| Ours 2D+3D              | 3DGS+LSeg    | 62.0 | 77.0 |

methods based on NeRF or 3DGS. We report mIoU and mAcc as the metrics of semantic segmentation on the ScanNet-20 benchmark. We compare our method on ScanNet dataset. ScanNet dataset has several canonical classes (wall, floor, table, *etc*.) with ground truth semantic labels on each posed 2D

TABLE II 3D OBJECT LOCALIZATION RESULTS ON LERF DATASET. WE FOLLOW LANGSPLAT [\[12\]](#page-10-30) TO REPORT LOCALIZATION ACCURACY (%) ON 4 SCENES.

| Scene         | LSeg | LERF | LangSplat | Ours (LSeg) | Ours (CLIP) |
|---------------|------|------|-----------|-------------|-------------|
| ramen         | 14.1 | 62.0 | 73.2      | 21.1        | 76.8        |
| figurines     | 8.9  | 75.0 | 80.4      | 10.7        | 83.1        |
| teatime       | 33.9 | 84.8 | 88.1      | 32.2        | 89.8        |
| waldo kitchen | 27.3 | 72.7 | 95.5      | 31.8        | 90.9        |
| overall       | 21.1 | 73.6 | 84.3      | 24.0        | 85.2        |

TABLE III PERFORMANCE OF ABLATION STUDIES.

<span id="page-6-1"></span>

| Setting             | mIoU | mAcc |
|---------------------|------|------|
| original            | 62.0 | 77.0 |
| XYZ+RGB features    | 58.9 | 74.7 |
| 20% Gaussian points | 61.2 | 76.1 |
| 10% input views     | 59.8 | 75.2 |

image. As we only process off-the-shelf 3D Gaussians and do not care about their training process, we do not need to report metrics about rendering quality. The training of 3D Gaussian Splatting follows the official setting. In our method, we extract

![](_page_7_Figure_1.jpeg)

<span id="page-7-0"></span>Fig. 5. Qualitative results of spatiotemporal tracking on the CMU Panoptic dataset. We choose 4 scenes with humans and dynamic objects to show the tracking performance.

semantic features from LSeg to conduct 2D projection and 3D network training. Consequently, the result in this section will show how much our method will improve from 2D visionlanguage models.

Table [I](#page-6-0) shows the performance of different methods. It can be observed that our Semantic Gaussians surpasses all open-vocabulary methods in mIoU and mAcc, and closely approaches the performance of state-of-the-art closed-set methods. This demonstrates that our approach effectively facilitates 3D scene understanding. We can also observe that both our 2D projection (Sec. [III-B\)](#page-3-1) and our 3D network (Sec. [III-C\)](#page-4-0) surpass the pre-trained LSeg model, even though all of our knowledge comes from it and relies on no ground truth labels. We assume the reason lies in the multi-view information integration, keeping the prediction consistent and mitigating some errors in low-quality views. Moreover, we notice that though the mIou and mAcc of our 3D network are lower than the 2D projection, the 2D and 3D ensemble will further improve our performance. We conjecture that some objects in certain scenes cannot be correctly recognized by 2D models in all views due to their low quality, while the 3D network could recognize them by utilizing geometric details.

Fig. [3](#page-5-1) shows the segmentation results of open-vocabulary methods based on NeRF and 3DGS on the ScanNet dataset. As shown, LERF and LangSplat exhibit low segmentation accuracy. This is primarily because they utilize multi-scale CLIP features for scene understanding, while CLIP features struggle to align precisely with the scene at the pixel level, making them unsuitable for generating pixel-level semantic segmentation maps. On the other hand, PVLFF, Feature 3DGS, and Semantic Gaussians all employ LSeg to achieve openvocabulary scene understanding. PVLFF performs relatively poorly and also suffers from slow rendering speeds as a NeRF-based method. Feature 3DGS and our method yield very similar performance, with Feature 3DGS even achieving more precise segmentation in certain views. However, Feature 3DGS requires retraining the semantic 3DGS for each scene, which is less efficient and flexible compared to our method.

*2) Object Localization:* Subsequently, we evaluated our method on the 3D object localization task across 4 scenes. Note that the LSeg model performed poorly on this task, significantly lagging behind CLIP-based methods like LERF and LangSplat. This likely lies in the fact that LSeg lacks the ability to recognize and segment long-tail objects, making it ineffective in locating objects within this dataset. Therefore, results of other LSeg-based methods are not included in the table. Fortunately, our method is not restricted by the 2D pretrained model and can utilize SAM as a mask generator, combining it with the CLIP model to achieve versatile projection. Our Semantic Gaussians based on SAM+CLIP outperformed in 3 out of 4 scenarios in the segmentation task and achieved the highest average accuracy, demonstrating the effectiveness and flexibility of our method.

![](_page_8_Figure_1.jpeg)

<span id="page-8-0"></span>Fig. 6. Visualization performance of VLPart [\[20\]](#page-10-12) on CMU Panoptic dataset. The failure cases are highlighted by red boxes.

*3) Ablation Study:* We conduct ablation studies to figure out the efficiency of our method. As the performance of 2D projection and 3D network is presented in Sec. [IV-B1,](#page-5-0) in this section, we ablate the performance of reducing 3D network input features, Gaussian points and input views. Points in 3D Gaussian Splatting have many features, *i.e*., coordinates, colors, rotations, scales, and opacities. If we only use coordinates and colors, they degrade to point clouds. Table [III](#page-6-1) shows the comparisons of different inputs. We observe that if we reduce the input features, the mIoU and mAcc of our 3D networks will become much lower. This implies that the extra features in 3D Gaussian Splatting are important, and provide more information than RGB point clouds. Table [III](#page-6-1) also shows the impact of reducing the number of Gaussian points and the number of input views, although these effects are less significant than reducing the input dimensions of the 3D network. This indicates that our method maintains a certain level of robustness even when there are fewer Gaussian points or input views, without suffering severe performance degradation.

### *C. Qualitative Evaluations*

*1) Part Segmentation:* In this section, we show the application of our Semantic Gaussians on part segmentation. As OpenSeg cannot tell object parts correctly, here we extract features from VLPart [\[20\]](#page-10-12) and use SAM [\[50\]](#page-11-6) to refine the segmentation result. The experiments are conducted on the MVImgNet dataset, which has different types of single objects suitable for part segmentation. The MVImgNet dataset does not have ground truth segmentations, so we compare our methods with other baseline models. Specifically, we compare our method with 2D vision-language models including OpenSeg and VLPart, and LERF [\[5\]](#page-10-4), a NeRF-based method that distills knowledge from multi-scale CLIP.

Fig. [4](#page-6-2) shows the qualitative result of part segmentation. From the result, we find that OpenSeg and LERF cannot distinguish object parts correctly, as their capabilities are limited by their training data. By contrast, VLPart is trained on object part segmentation dataset and it can tell parts effectively. However, VLPart cannot keep segmentation consistency across different views, while our Semantic Gaussians distills knowledge from VLPart, and can keep high-quality segmentations in all views.

![](_page_8_Figure_7.jpeg)

<span id="page-8-1"></span>Fig. 7. Visualization results of instance segmentation results on 3 different scenes. We show the segmentation result of DEVA and our Semantic Gaussians. Different colors in the segmentation map denote different instances.

*2) Spatiotemporal Tracking:* In this section, we show the performance of our Semantic Gaussians on spatiotemporal tracking. 3D Gaussian Splatting is originally designed to represent a static scene, while some succeeding works [\[24\]](#page-10-16), [\[30\]](#page-10-22), [\[57\]](#page-11-13) ameliorate it to support 4D dynamic scenes. We follow the work of Dynamic 3D Gaussians [\[24\]](#page-10-16) to represent a spatiotemporal scene and use their pre-trained scenes from the CMU Panoptic dataset [\[52\]](#page-11-8) to evaluate our tracking performance.

Fig. [5](#page-7-0) shows the qualitative result of our spatiotemporal tracking. As the scene often contains 12 humans and a ˜ dynamic object, we use VLPart in 2D projection and perform human part segmentation simultaneously. For each dynamic 3D Gaussian, we conduct our method at every frame to avoid looking at future frames. We render some novel views to show our capability of spatial tracking. The results show that our Semantic Gaussians can track human parts and objects with a high accuracy between different views and timesteps.

We also tried to segment each image individually from the same viewpoint by VLPart, and the results are shown in the Fig. [6.](#page-8-0) It can be observed that, although VLPart is able to produce fine boundaries, it makes different errors at different viewpoints or timesteps (highlighted in red boxes in the figure). This lack of spatiotemporal consistency in VLPart's results makes it difficult to achieve spatiotemporal tracking. In contrast, our method, which is based on 4D Gaussians as the representation, inherently possesses strong consistency, enabling more accurate tracking.

*3) Scene-Level Instance Segmentation:* In this section, we will show the performance of Semantic Gaussians on scenelevel instance segmentation tasks. Some related works [\[58\]](#page-11-14)– [\[60\]](#page-11-15) utilize SAM to generate weakly supervised masks and endow 3DGS with instance segmentation capabilities by redesigning the loss function and training 3DGS. Similarly, our method can leverage the knowledge from SAM to assign instance labels to 3DGS through a single projection. Specifically, following the approach of [\[58\]](#page-11-14), we use DEVA [\[61\]](#page-11-16) as the

![](_page_9_Figure_1.jpeg)

<span id="page-9-0"></span>Fig. 8. Qualitative examples of language-guided editing. We perform object removal, movement, and color change on Mip-NeRF 360 room scene.

scene-level mask generator. DEVA is capable of assigning a unique scene-level ID to each object in a video, and we project this ID in a one-hot manner directly onto 3DGS. By rendering the semantic channels of 3DGS, instance segmentation maps from any viewpoint can be obtained.

Fig. [7](#page-8-1) illustrates the visualization results of our method on the instance segmentation task. We choose 3 scenes from different datasets including LERF [\[5\]](#page-10-4), 3D-OVS [\[4\]](#page-10-3) and Mip-NeRF 360 [\[53\]](#page-11-9). It can be observed that our method can accurately delineate the boundaries of foreground objects with high precision without any retraining of 3DGS. However, for background objects or those that appear infrequently, our method fails to yield accurate boundaries and instance classifications. The primary reason is that DEVA, as a pre-trained model, cannot ensure the consistency of IDs for the background across different viewpoints. Our method can combine the segmentation results of DEVA from different viewpoints to achieve more consistent 3D instance segmentation results.

*4) Language-guided Editing:* In this section, we show the application of language-guided editing of our Semantic Gaussians. There are several works [\[13\]](#page-10-31), [\[58\]](#page-11-14), [\[62\]](#page-11-17)–[\[65\]](#page-11-18) that segments 3DGS by SAM and conduct instance editing, but they often require the retraining of 3DGS. Our method can predict semantic embeddings for each 3D Gaussian point, and thus we can choose certain points by language query. We define some canonical operations such as removing, moving and color changing, and employ a language encoder to select the target Gaussians.

Fig. [8](#page-9-0) shows some qualitative examples of language-guided editing on the room scene in the Mip-NeRF 360 dataset [\[53\]](#page-11-9). In these examples, we use CLIP text embeddings of "glass bottle", "metal bowl" and "slippers" to query and choose certain 3D Gaussian points in the scene, and we edit them by modifying their properties such as coordinates, colors, opacities, *etc*. From these examples, we observe that the language guidance can accurately select the target object, and thus we can perform various editing operations on the selected 3D Gaussians.

## V. CONCLUSION

In this work, we propose Semantic Gaussians, a novel approach to open-vocabulary 3D scene understanding via 3D Gaussian Splatting. Semantic Gaussians distill knowledge from pre-trained 2D encoders by projecting 2D pixel-level embeddings to 3D Gaussian points. Moreover, we introduce a 3D sparse convolutional network to predict semantic components with the input of RGB Gaussians, thus achieving zero-shot generalization to unseen 3D scenes. We conduct experiments on the ScanNet segmentation benchmark to prove its effectiveness and exhibit downstream applications such as part segmentation, spatiotemporal tracking, instance segmentation, and scene editing. Our work paves the way for realworld applications of 3D Gaussian Splatting, such as embodied agents and augmented reality systems.

Albeit the advantages we have demonstrated, our Semantic Gaussians framework does have limitations. The scene understanding performance is bottlenecked by the performance of 2D pre-trained models and off-the-shelf 3D Gaussians. On the one hand, if the 2D pre-trained model completely fails to recognize the scene, Semantic Gaussians will fail either. Our proposed 3D semantic network can help lift the performances to some extent. Further, we may reconcile features from multiple 2D pre-trained encoders. On the other hand, if the 3D Gaussians cannot generalize well to a needed novel view, *i.e*., the 3D Gaussian-based scene representation is weak, Semantic Gaussians will not be able to provide robust scene understanding with that novel view as well. This limitation belongs to 3D Gaussian Splatting, as we do not modify any property of 3D Gaussians. Fortunately, 3D Gaussian Splatting is gaining much popularity recently, and we believe the progress made on 3D Gaussian Splatting will improve the performance of our Semantic Gaussians.

## REFERENCES

- <span id="page-10-0"></span>[1] H. Ha and S. Song, "Semantic abstraction: Open-world 3d scene understanding from 2d vision-language models," in *CoRL*, 2022.
- <span id="page-10-1"></span>[2] S. Peng, K. Genova, C. Jiang, A. Tagliasacchi, M. Pollefeys, T. Funkhouser *et al.*, "Openscene: 3d scene understanding with open vocabularies," in *CVPR*, 2023, pp. 815–824.
- <span id="page-10-2"></span>[3] A. Takmaz, E. Fedele, R. W. Sumner, M. Pollefeys, F. Tombari, and F. Engelmann, "Openmask3d: Open-vocabulary 3d instance segmentation," *arXiv preprint arXiv:2306.13631*, 2023.
- <span id="page-10-3"></span>[4] K. Liu, F. Zhan, J. Zhang, M. Xu, Y. Yu, A. El Saddik, C. Theobalt, E. Xing, and S. Lu, "Weakly supervised 3d open-vocabulary segmentation," *NeurIPS*, vol. 36, 2024.
- <span id="page-10-4"></span>[5] J. Kerr, C. M. Kim, K. Goldberg, A. Kanazawa, and M. Tancik, "Lerf: Language embedded radiance fields," in *ICCV*, 2023, pp. 19 729–19 739.
- <span id="page-10-5"></span>[6] J.-B. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds *et al.*, "Flamingo: a visual language model for few-shot learning," *NeurIPS*, 2022.
- <span id="page-10-6"></span>[7] B. Kerbl, G. Kopanas, T. Leimkuhler, and G. Drettakis, "3d gaussian ¨ splatting for real-time radiance field rendering," *ACM Transactions on Graphics*, vol. 42, no. 4, 2023.
- <span id="page-10-7"></span>[8] S. Kobayashi, E. Matsumoto, and V. Sitzmann, "Decomposing nerf for editing via feature field distillation," *Advances in Neural Information Processing Systems*, vol. 35, pp. 23 311–23 330, 2022.
- [9] Z. Fan, P. Wang, Y. Jiang, X. Gong, D. Xu, and Z. Wang, "Nerfsos: Any-view self-supervised object segmentation on complex scenes," *arXiv preprint arXiv:2209.08776*, 2022.
- [10] V. Tschernezki, I. Laina, D. Larlus, and A. Vedaldi, "Neural feature fusion fields: 3d distillation of self-supervised 2d image representations," in *2022 International Conference on 3D Vision (3DV)*. IEEE, 2022, pp. 443–453.
- <span id="page-10-29"></span>[11] G. Liao, K. Zhou, Z. Bao, K. Liu, and Q. Li, "Ov-nerf: Open-vocabulary neural radiance fields with vision and language foundation models for 3d semantic understanding," *arXiv preprint arXiv:2402.04648*, 2024.
- <span id="page-10-30"></span>[12] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, "Langsplat: 3d language gaussian splatting," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 20 051–20 060.
- <span id="page-10-31"></span>[13] S. Zhou, H. Chang, S. Jiang, Z. Fan, Z. Zhu, D. Xu, P. Chari, S. You, Z. Wang, and A. Kadambi, "Feature 3dgs: Supercharging 3d gaussian splatting to enable distilled feature fields," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 676–21 685.
- [14] G. Liao, J. Li, Z. Bao, X. Ye, J. Wang, Q. Li, and K. Liu, "Clip-gs: Clip-informed gaussian splatting for real-time and view-consistent 3d semantic understanding," *arXiv preprint arXiv:2404.14249*, 2024.
- [15] X. Zuo, P. Samangouei, Y. Zhou, Y. Di, and M. Li, "Fmgs: Foundation model embedded 3d gaussian splatting for holistic 3d scene understanding," *arXiv preprint arXiv:2401.01970*, 2024.
- <span id="page-10-8"></span>[16] J.-C. Shi, M. Wang, H.-B. Duan, and S.-H. Guan, "Language embedded 3d gaussians for open-vocabulary scene understanding," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 5333–5343.
- <span id="page-10-9"></span>[17] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark *et al.*, "Learning transferable visual models from natural language supervision," in *ICML*. PMLR, 2021, pp. 8748–8763.
- <span id="page-10-10"></span>[18] B. Li, K. Q. Weinberger, S. J. Belongie, V. Koltun, and R. Ranftl, "Language-driven semantic segmentation," in *ICLR*, 2022.
- <span id="page-10-11"></span>[19] G. Ghiasi, X. Gu, Y. Cui, and T.-Y. Lin, "Scaling open-vocabulary image segmentation with image-level labels," in *ECCV*. Springer, 2022, pp. 540–557.
- <span id="page-10-12"></span>[20] P. Sun, S. Chen, C. Zhu, F. Xiao, P. Luo, S. Xie, and Z. Yan, "Going denser with open-vocabulary part segmentation," *arXiv preprint arXiv:2305.11173*, 2023.

- <span id="page-10-13"></span>[21] C. Choy, J. Gwak, and S. Savarese, "4d spatio-temporal convnets: Minkowski convolutional neural networks," in *CVPR*, 2019, pp. 3075– 3084.
- <span id="page-10-14"></span>[22] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, "Scannet: Richly-annotated 3d reconstructions of indoor scenes," in *CVPR*, 2017, pp. 5828–5839.
- <span id="page-10-15"></span>[23] X. Yu, M. Xu, Y. Zhang, H. Liu, C. Ye, Y. Wu, Z. Yan, C. Zhu, Z. Xiong, T. Liang *et al.*, "Mvimgnet: A large-scale dataset of multi-view images," in *CVPR*, 2023, pp. 9150–9161.
- <span id="page-10-16"></span>[24] J. Luiten, G. Kopanas, B. Leibe, and D. Ramanan, "Dynamic 3d gaussians: Tracking by persistent dynamic view synthesis," *arXiv preprint arXiv:2308.09713*, 2023.
- <span id="page-10-17"></span>[25] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, "Nerf: Representing scenes as neural radiance fields for view synthesis," *Communications of the ACM*, vol. 65, no. 1, pp. 99–106, 2021.
- <span id="page-10-18"></span>[26] S. Zhi, T. Laidlow, S. Leutenegger, and A. J. Davison, "In-place scene labelling and understanding with implicit scene representation," in *CVPR*, 2021, pp. 15 838–15 847.
- <span id="page-10-19"></span>[27] S. Liu, X. Zhang, Z. Zhang, R. Zhang, J.-Y. Zhu, and B. Russell, "Editing conditional radiance fields," in *CVPR*, 2021, pp. 5773–5783.
- <span id="page-10-20"></span>[28] C. Gao, A. Saraf, J. Kopf, and J.-B. Huang, "Dynamic view synthesis from dynamic monocular video," in *CVPR*, 2021, pp. 5712–5721.
- <span id="page-10-21"></span>[29] A. Pumarola, E. Corona, G. Pons-Moll, and F. Moreno-Noguer, "Dnerf: Neural radiance fields for dynamic scenes," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2021, pp. 10 318–10 327.
- <span id="page-10-22"></span>[30] G. Wu, T. Yi, J. Fang, L. Xie, X. Zhang, W. Wei, W. Liu, Q. Tian, and X. Wang, "4d gaussian splatting for real-time dynamic scene rendering," *arXiv preprint arXiv:2310.08528*, 2023.
- [31] Z. Yang, H. Yang, Z. Pan, X. Zhu, and L. Zhang, "Real-time photorealistic dynamic scene representation and rendering with 4d gaussian splatting," *arXiv preprint arXiv:2310.10642*, 2023.
- [32] Y. Lin, Z. Dai, S. Zhu, and Y. Yao, "Gaussian-flow: 4d reconstruction with dynamic 3d gaussian particle," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 136–21 145.
- <span id="page-10-24"></span>[33] W.-H. Chu, L. Ke, and K. Fragkiadaki, "Dreamscene4d: Dynamic multi-object scene generation from monocular videos," *arXiv preprint arXiv:2405.02280*, 2024.
- <span id="page-10-23"></span>[34] H. Ling, S. W. Kim, A. Torralba, S. Fidler, and K. Kreis, "Align your gaussians: Text-to-4d with dynamic 3d gaussians and composed diffusion models," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 8576–8588.
- [35] Z. Chen, F. Wang, Y. Wang, and H. Liu, "Text-to-3d using gaussian splatting," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 401–21 412.
- [36] S. Zhou, Z. Fan, D. Xu, H. Chang, P. Chari, T. Bharadwaj, S. You, Z. Wang, and A. Kadambi, "Dreamscene360: Unconstrained text-to-3d scene generation with panoramic gaussian splatting," *arXiv preprint arXiv:2404.06903*, 2024.
- [37] J. Tang, J. Ren, H. Zhou, Z. Liu, and G. Zeng, "Dreamgaussian: Generative gaussian splatting for efficient 3d content creation," in *The Twelfth International Conference on Learning Representations*, 2024.
- [38] Y. Liang, X. Yang, J. Lin, H. Li, X. Xu, and Y. Chen, "Luciddreamer: Towards high-fidelity text-to-3d generation via interval score matching," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 6517–6526.
- <span id="page-10-25"></span>[39] X. Liu, X. Zhan, J. Tang, Y. Shan, G. Zeng, D. Lin, X. Liu, and Z. Liu, "Humangaussian: Text-driven 3d human generation with gaussian splatting," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 6646–6657.
- <span id="page-10-26"></span>[40] F. Liang, B. Wu, X. Dai, K. Li, Y. Zhao, H. Zhang, P. Zhang, P. Vajda, and D. Marculescu, "Open-vocabulary semantic segmentation with mask-adapted clip," in *CVPR*, 2023, pp. 7061–7070.
- <span id="page-10-27"></span>[41] H. Luo, J. Bao, Y. Wu, X. He, and T. Li, "Segclip: Patch aggregation with learnable centers for open-vocabulary semantic segmentation," in *ICML*. PMLR, 2023, pp. 23 033–23 044.
- <span id="page-10-28"></span>[42] K. M. Jatavallabhula, A. Kuwajerwala, Q. Gu, M. Omama, T. Chen, A. Maalouf, S. Li, G. Iyer, S. Saryazdi, N. Keetha *et al.*, "Conceptfusion: Open-set multimodal 3d mapping," *arXiv preprint arXiv:2302.07241*, 2023.
- [43] R. Ding, J. Yang, C. Xue, W. Zhang, S. Bai, and X. Qi, "Pla: Languagedriven open-vocabulary 3d scene understanding," in *CVPR*, 2023, pp. 7010–7019.

- <span id="page-11-0"></span>[44] J. Zhang, R. Dong, and K. Ma, "Clip-fo3d: Learning free open-world 3d scene representations from 2d dense clip," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 2048–2059.
- <span id="page-11-1"></span>[45] Y. Siddiqui, L. Porzi, S. R. Bulo, N. M ` uller, M. Nießner, A. Dai, and ¨ P. Kontschieder, "Panoptic lifting for 3d scene understanding with neural fields," in *CVPR*, 2023, pp. 9043–9052.
- <span id="page-11-2"></span>[46] Y. Bhalgat, I. Laina, J. F. Henriques, A. Zisserman, and A. Vedaldi, "Contrastive lift: 3d object instance segmentation by slow-fast contrastive fusion," *arXiv preprint arXiv:2306.04633*, 2023.
- <span id="page-11-3"></span>[47] M. Caron, H. Touvron, I. Misra, H. Jegou, J. Mairal, P. Bojanowski, and ´ A. Joulin, "Emerging properties in self-supervised vision transformers," in *ICCV*, 2021, pp. 9650–9660.
- <span id="page-11-4"></span>[48] J. L. Schonberger and J.-M. Frahm, "Structure-from-motion revisited," in *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2016, pp. 4104–4113.
- <span id="page-11-5"></span>[49] S. Liu, Z. Zeng, T. Ren, F. Li, H. Zhang, J. Yang, C. Li, J. Yang, H. Su, J. Zhu *et al.*, "Grounding dino: Marrying dino with grounded pretraining for open-set object detection," *arXiv preprint arXiv:2303.05499*, 2023.
- <span id="page-11-6"></span>[50] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo *et al.*, "Segment anything," *arXiv preprint arXiv:2304.02643*, 2023.
- <span id="page-11-7"></span>[51] T. Ren, S. Liu, A. Zeng, J. Lin, K. Li, H. Cao, J. Chen, X. Huang, Y. Chen, F. Yan *et al.*, "Grounded sam: Assembling open-world models for diverse visual tasks," *arXiv preprint arXiv:2401.14159*, 2024.
- <span id="page-11-8"></span>[52] H. Joo, H. Liu, L. Tan, L. Gui, B. Nabbe, I. Matthews, T. Kanade, S. Nobuhara, and Y. Sheikh, "Panoptic studio: A massively multiview system for social motion capture," in *Proceedings of the IEEE International Conference on Computer Vision*, 2015, pp. 3334–3342.
- <span id="page-11-9"></span>[53] J. T. Barron, B. Mildenhall, D. Verbin, P. P. Srinivasan, and P. Hedman, "Mip-nerf 360: Unbounded anti-aliased neural radiance fields," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2022, pp. 5470–5479.
- <span id="page-11-10"></span>[54] B. Cheng, I. Misra, A. G. Schwing, A. Kirillov, and R. Girdhar, "Masked-attention mask transformer for universal image segmentation," in *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, 2022, pp. 1290–1299.
- <span id="page-11-11"></span>[55] B. Wang, L. Chen, and B. Yang, "Dm-nerf: 3d scene geometry decomposition and manipulation from 2d images," *arXiv preprint arXiv:2208.07227*, 2022.
- <span id="page-11-12"></span>[56] H. Chen, K. Blomqvist, F. Milano, and R. Siegwart, "Panoptic visionlanguage feature fields," *IEEE Robotics and Automation Letters*, 2024.
- <span id="page-11-13"></span>[57] Z. Li, Z. Chen, Z. Li, and Y. Xu, "Spacetime gaussian feature splatting for real-time dynamic view synthesis," *arXiv preprint arXiv:2312.16812* , 2023.
- <span id="page-11-14"></span>[58] M. Ye, M. Danelljan, F. Yu, and L. Ke, "Gaussian grouping: Segment and edit anything in 3d scenes," *arXiv preprint arXiv:2312.00732*, 2023.
- [59] X. Hu, Y. Wang, L. Fan, J. Fan, J. Peng, Z. Lei, Q. Li, and Z. Zhang, "Semantic anything in 3d gaussians," *arXiv preprint arXiv:2401.17857* , 2024.
- <span id="page-11-15"></span>[60] J. Cen, J. Fang, C. Yang, L. Xie, X. Zhang, W. Shen, and Q. Tian, "Segment any 3d gaussians," *arXiv preprint arXiv:2312.00860*, 2024.
- <span id="page-11-16"></span>[61] H. K. Cheng, S. W. Oh, B. Price, A. Schwing, and J.-Y. Lee, "Tracking anything with decoupled video segmentation," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 1316–1326.
- <span id="page-11-17"></span>[62] X. Hu, Y. Wang, L. Fan, J. Fan, J. Peng, Z. Lei, Q. Li, and Z. Zhang, "Semantic anything in 3d gaussians," *arXiv preprint arXiv:2401.17857* , 2024.
- [63] J. Wang, J. Fang, X. Zhang, L. Xie, and Q. Tian, "Gaussianeditor: Editing 3d gaussians delicately with text instructions," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition* , 2024, pp. 20 902–20 911.
- [64] Y. Chen, Z. Chen, C. Zhang, F. Wang, X. Yang, Y. Wang, Z. Cai, L. Yang, H. Liu, and G. Lin, "Gaussianeditor: Swift and controllable 3d editing with gaussian splatting," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 21 476–21 485.
- <span id="page-11-18"></span>[65] M. C. Silva, M. Dahaghin, M. Toso, and A. Del Bue, "Contrastive gaussian clustering: Weakly supervised 3d scene segmentation," *arXiv preprint arXiv:2404.12784*, 2024.