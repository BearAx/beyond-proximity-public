# Beyond *Bare* Queries: Open-Vocabulary Object Grounding with 3D Scene Graph

Sergey Linok<sup>1,\*,†</sup>, Tatiana Zemskova<sup>1,2,\*</sup>, Svetlana Ladanova<sup>1</sup>, Roman Titkov<sup>1</sup>, Dmitry Yudin<sup>1,2</sup>, Maxim Monastyrny<sup>3</sup>, Aleksei Valenkov<sup>3</sup>

Abstract—Locating objects described in natural language presents a significant challenge for autonomous agents. Existing CLIP-based open-vocabulary methods successfully perform 3D object grounding with simple (bare) queries, but cannot cope with ambiguous descriptions that demand an understanding of object relations. To tackle this problem, we propose a modular approach called BBQ (Beyond Bare Queries), which constructs 3D scene graph representation with metric and semantic spatial edges and utilizes a large language model as a human-toagent interface through our deductive scene reasoning algorithm. BBQ employs robust DINO-powered associations to construct 3D object-centric map and an advanced raycasting algorithm with a 2D vision-language model to describe them as graph nodes. On the Replica and ScanNet datasets, we have demonstrated that BBQ takes a leading place in openvocabulary 3D semantic segmentation compared to other zeroshot methods. Also, we show that leveraging spatial relations is especially effective for scenes containing multiple entities of the same semantic class. On challenging Sr3D+, Nr3D and ScanRefer benchmarks, our deductive approach demonstrates a significant improvement, enabling objects grounding by complex queries compared to other state-of-the-art methods. The combination of our design choices and software implementation has resulted in significant data processing speed in experiments on the robot on-board computer. This promising performance enables the application of our approach in intelligent robotics projects. We made the code publicly available at linukc.github.io/BeyondBareQueries.

### I. INTRODUCTION

Open-vocabulary 3D perception is a primary challenge for advanced AI-powered autonomous agents. For instance, locating a referred object based on a complex text query in an environment full of semantically similar distractors remains an unsolved question.

The effective combination of vision and text modalities has been a subject of intensive study in the research field, with a particular focus on CLIP-based [1]–[6] encoders and more advanced visual foundation models [7]–[9], [9]–[11], [11]–[16]. To address object inter-relations in complex 3D environments, scene graph representations have emerged as the most promising approach [17]–[20]. Scene edges are described as embeddings or text, allowing rich and finegrained representations of spatial and semantic relationships. Large language models (LLMs) are increasingly being utilized in 3D perception as tools capable of sophisticated

<span id="page-0-0"></span>![](_page_0_Picture_12.jpeg)

Fig. 1. Proposed *BBQ* approach leverages foundation models for high-performance construction of an object-centric class-agnostic 3D map of a static indoor environment from a sequence of RGB-D frames with known camera poses and calibration. To perform scene understanding, we represent environment as a set of nodes with spatial relations. Utilizing a designed *deductive* scene reasoning algorithm, our method enable efficient natural language interaction with a scene-aware large language model.

reasoning [19]–[26]. Leveraging the power of scene graph representation as input, such systems can robustly interpret queries with the power of inner knowledge and accurately respond about scene-specific objects or locations, opening up new possibilities for applications in robotics, augmented reality, and intelligent assistive technologies. Despite the impressive qualities exhibited by these approaches, significant challenges remain in the field.

In our research, we particularly focus on approaches that exploit generalization ability of pretrained models to perform open-vocabulary 3D grounding in a zero-shot manner from an RGB-D sequence. The first challenge for the aforementioned methods is the difficulty in accumulating reliable visual/text representations for scene objects with a low resource cost on a robot on-board computers. The second challenge is to preserve scene spatial awareness in both view-dependent and view-independent object relations. The third challenge is how to effectively incorporate 3D scene representation and query a large language model to perform the desired task.

To address these challenges, we explicitly separate the 3D objects mapping process from object visual/text encoding. Self-supervised DINO image embeddings have proven to be robust discriminative features that are sufficient for strong 2.5D understanding [27]–[30]. For each frame, we extract these deep features and employ fast DINO-based proposals-to-objects accumulation (Sec. III-A). At the end of a sequence, to select a projection frame for 2D captioning we perform a designed multiview clustering technique (Sec. III-B), that drastically reduces the search space (Sec. III-C).

In order to maintain spatial awareness in a scene graph, we incorporate both metric and semantic spatial edges (Sec.

<sup>&</sup>lt;sup>1</sup>Center for Cognitive Modeling, Moscow Institute of Physics and Technology, Dolgoprudny, Russia

<sup>&</sup>lt;sup>2</sup>AIRI, Moscow, Russia

<sup>&</sup>lt;sup>3</sup>Sberbank of Russia, Robotics Center, Moscow, Russia

<sup>†</sup>Corresponding author: linok.sa@phystech.edu

<sup>\*</sup>Equal contribution

III-D). Inspired by the chain-of-thought technique [31], we propose a two-stage deductive scene reasoning algorithm for object grounding (Sec. III-E). In the first stage, an LLM selects potential target and anchor objects for a user query based solely on object descriptions (Sec. III-E, Fig. 1). This not only reduces the search space but also minimizes the number of edges constructed. In the second stage, the LLM makes the final prediction, utilizing additional information regarding the spatial positions of both targets and anchors, as well as the edges connecting them.

To summarize, the contributions of this paper include:

- high-performance DINO-based 3D object-centric map construction algorithm from a sequence of posed RGB-D images (Sec. III-A, Sec. III-B);
- cheap to construct and descriptive rich 3D scene graph representation with metric and semantic spatial edges (Sec. III-C, Sec. III-D);
- deductive scene reasoning algorithm to use our scene graph representation with large language model for open-vocabulary 3D object grounding (Sec. III-E);
- integration of these capabilities in a single modular method called BBQ. We make the code publicly available at linukc.github.io/BeyondBareQueries.

### II. RELATED WORKS

### A. Open-Vocabulary 3D Segmentation

Open-vocabulary segmentation gives the ability to locate an arbitrary semantic category on a scene. The key challenge in working with 3D data is efficient encoding of aligned visual/text embeddings [1]–[13] in scene reconstruction. Most modern methods project 2D features into 3D [20], [23], [32]–[36], perform 2D-to-3D pointwise distillation [24], [37], combine both approaches [18], [19], [25], [38]–[42], or use advanced scene-specific representations such as NeRF [43]–[47] and Gaussian Splatting [48]–[50] with auxiliary 2D supervision. To obtain reliable 2D features that describe more than just the local context, various techniques are applied, such as sliding window averaging [40], class-agnostic mask cropping [20], superpixel grouping [51].

Final 3D features can be represented in different format: one feature by point [34], voxel [52], object [20]. The last format allows the answer to be aligned with some scene instance with the closest similarity to the query. In contrast, other representations will always return some part of the environment with a similarity higher than a defined threshold.

### B. 3D Scene Graphs

3D scene graph provides a compact and structured representation of the environment, capturing not only the objects but also their spatial arrangements and semantic relationships. 3D scene graph can be obtained from known 3D geometries [17], [19], [53] or fused from RGB sequence as a combination of local 2D scene graphs [13], [54]. Nodes and edges can belong to a fixed set of semantic categories [55], [56] or be predicted in an open-vocabulary manner [18], [20], [57] allowing transfer to unseen environments without additional fine-tuning. Graphs can describe one-level relations

(for example, objects-objects) [54], [58], [59] or contain a hierarchical representation [19], [53], [60].

### C. 3D Object Grounding

3D object grounding aims to find a particular instance in a scene, described in a natural language query. The query can contain references to other objects or a specific location [61], [62], an affordance reference [63], [64], or other types of object attributes [62]. Solving this task involves understanding the relationships between objects. It can be done with interpretable 3D scene graphs [20], [65] or learned with supervision from annotation [66]–[68].

Integrating an LLM into a perception pipeline can provide a source of domain knowledge that enables complex query understanding and reasoning. Different approaches use an LLM simply as an interface, providing scene-specific description in an input context [69], [70], or performing finetuning [24], [64], [71], [72]. To add the ability to perceive the visual modality, these methods use pre-trained point cloud encoders [24], [64], [71] or train them to align with the text modality [72]. Then the authors perform instruction tuning of the projection layers [24], [71], [72] or additionally fine-tune the LLM [64].

Unlike existing 3D Object Grounding methods that integrate LLMs, our approach does not rely on ground-truth scene point clouds or domain-specific fine-tuning [73]. Instead, we build a 3D scene graph on-the-fly from a sequence of posed RGBD images, using only foundation models, enabling easy transfer to unseen environments. We also show that our method, combined with the *deductive* scene reasoning algorithm outperforms the similar baselines ConceptGraphs [20] and LLM-Grounder [70].

Our work is conceptually closest to ConceptGraphs [20], however each of our contribution identifies gap in existing methodology and suggest novel solution. We show in the experiment section that it is not only improve overall quality (Sec. IV), but also significantly reduce required computational resources and allow to apply BBQ in real-life scenarios (Sec. IV-C).

### III. METHOD

### <span id="page-1-0"></span>A. Object-centric 3D map construction (3D Mapping)

For each input RGB-D frame I with a resolution  $H \times W$  pretrained foundation model extract set of 2D proposal (boolean masks)  $M \in \mathbb{R}^{H \times W}$  and DINO embeddings  $E_{DINO} \in \mathbb{R}^{H/s \times W/s \times dim}$ , where s is DINO transformer patch stride. For M we experimented with MobileSAMv2 [74], for  $E_{DINO}$ , we examined DINOv2 with registers [75].

After a series of filtration checks to discard low confidence, small or too large regions, each passed mask m is represented as point cloud  $p \in \mathbb{R}^{N \times 3}$ , where N - number of points in mask that we project based of depth information, pose and camera calibration. To point cloud p we additionally apply DBSCAN to remove noise from inaccurate 2D proposal m. Associated descriptor  $d \in \mathbb{R}^{dim}$  is extracted from  $E_{DINO}$  by averaging all features in interpolated to  $R^{H/s \times W/s}$  mask m. Each frame I from sequence of images

![](_page_2_Figure_0.jpeg)

Fig. 2. An object-centric class-agnostic 3D map is iteratively constructed from a sequence of RGB-D camera frames and their poses by associating 2D MobileSAMv2 mask proposals with 3D objects with deep DINOv2 visual features and spatial constraints (Sec. III-A). To visually represent objects after building the map, we select the *best* view based on the largest projected mask from L cluster centroids that represent areas of object observations (Sec. III-B). We leverage LLaVA1.6 [15] and text-aligned visual encoder EVA2 [3] to describe object visual properties (Sec. III-C). With the node's text descriptions, spatial locations, metric and semantic spatial edges (Sec. III-D) we utilize LLM in our *deductive* reasoning algorithm (Sec. III-E) to perform a 3D object grounding task.

is represented by detection set  $\{(p_k, d_k) \mid k \in (1, \dots, K)\}$ , where K - number of selected proposals.

To construct a class-agnostic object-centric 3D map on each frame we perform an association process between incoming detections set and objects on the scene. For the first frame, we simply initialize objects as detections. Association process consists of finding visual cosine similarities between all intersected instances. If for j-th detection  $CosineSimularity(d_i, d_i)$  lower than visual threshold  $\sigma_{vis}$ for every object i, we initialize this detection as a new object, else merge with closest by cosine similarity. During merging process we combine point clouds, increase number of detections for object, add frame index for future 3D to 2D projection search and update object visual descriptor with moving average. Assigning a higher weight to incoming descriptors leverages the capability of DINO features to effectively identify correspondences between local frames while preserving information for objects merging. To reduce the growing number of objects that appear after unsuccessful association each m-th, object merging with lower  $\sigma_{vis}$  and spatial overlap is called. After object map construction we perform the postprocessing step: filter objects to discard outliers (low points, size or number of detections).

### <span id="page-2-0"></span>B. Object best view 3D to 2D projection

Because performing the raycasting procedure for all poses is time-consuming, we decided to cluster 3D camera coordinates  $P_i = \{(x,y,z)_q \mid q \in (1,\ldots,Q)\}$  from Q viewpoints where we observed the object  $o_i$ , to L groups. Then, we select L poses closest to the centroids of the corresponding clusters, which represent centers of object observation. Our experiments demonstrate L=5 to be a sufficient number of observations on the indoor Replica and ScanNet datasets.

Then we select *best* object view based on the largest area of projection (Eq. 1):

<span id="page-2-4"></span><span id="page-2-3"></span>
$$\max_{P_l|l\in(1,\dots,L)} A\left(R(o_i, P_l)\right),\tag{1}$$

where R is the raycasting operator that converts an object's point cloud  $p_i$  in the pose  $P_l$  into mask, and A is the operator that estimates the area of the object's mask.

### <span id="page-2-1"></span>C. 3D scene graph node generation

To describe each object (node)  $o_i$  we utilize a visual language model and text-aligned visual encoder on a projected crop. Our internal experiments show that LLaVA1.6 [15] performs best for indoor scene captioning and EVA2 [3] for visual encoding. We call the captioning model with a prompt "Describe visible object in front of you, paying close attention to its spatial dimensions and visual attributes". We also incorporate enhanced environmental awareness in the prompt and several handcrafted examples.

### <span id="page-2-2"></span>D. 3D Scene graph edge generation

When generating scene graph edges, we pursue two goals: 1) enabling LLM to answer complex user queries, and 2) compactly describing object relations in textual form.

To achieve these goals, we define scene graph edges using two types of relations: metric relations  $d_{ij}$  and semantic relations  $s_{ij}$ . Metric relations are defined as Euclidean distances between the centers of objects' bounding boxes. Semantic relations include the following set: left, right, front, behind, above and below. Since the relations left, right, front, behind are view-dependent, they are defined independently for each grounding phrase using the heuristic algorithm from ZSVG3D [69]. For each grounding phrase, we define target

# Algorithm 1 Deductive scene reasoning algorithm $(O^{id}, O^{caption}, O^{center}, O^{extent}, query)$

```
(TargetIds, AnchorIds) \leftarrow LLM(query, O^{id}, O^{caption})
N_{target} \leftarrow \text{number of } TargetIds
N_{anchor} \leftarrow \text{number of } AnchorIds
RelatedObjects \leftarrow \emptyset
for i in range (0, N_{target}) do
o^{relations} \leftarrow \emptyset
for j in range (0, N_{anchor}) do
s_{ij} \leftarrow semantic.relation(o^{center}_i, o^{center}_j)
d_{ij} \leftarrow euclidean.distance(o^{center}_i, o^{center}_j)
E_{ij} \leftarrow (d_{ij}, s_{ij})
Append E_{ij} to o^{relations}_i
end for
Target \leftarrow \{o^{id}_i, o^{caption}_i, o^{center}_i, o^{extent}_i, o^{relations}_i\}
Append Target to RelatedObjects
end for
for j in range (0, N_{anchor}) do
Anchor \leftarrow \{o^{id}_i, o^{caption}_i, o^{center}_i, o^{extent}_i\}
Append Anchor to RelatedObjects
end for
FinalObjectId \leftarrow LLM(query, RelatedObjects)
```

and anchor objects (see Sec. III-E for more details). For each target-anchor pair, a virtual camera is placed at the room's center and pointed at the anchor. View-dependent relations are then determined based on the 2D projections of objects in the camera's egocentric view. Since the pairs of relations left/right, front/back, above/below are not mutually exclusive, a semantic spatial edge  $s_{ij}$  consists of a set of three relations that include one relation from each pair (e.g.  $s_{ij} = (left, front, above)$ ).

### <span id="page-3-0"></span>E. Applying scene graph to a LLM

We propose using an LLM and scene text description to locate objects by their open vocabulary references. We store the scene description as a JSON file containing an objects list O. For each object i, we store its id  $(o_i^{id})$ , caption  $(o_i^{caption})$ , center  $(o_i^{center})$  and extent  $(o_i^{extent})$  of its 3D bounding box. We construct list E of the objects connections for each user query independently. The relation between objects  $o_i$  and  $o_j$  includes  $o_i^{caption}$ ,  $o_i^{id}$ ,  $o_j^{caption}$ ,  $o_j^{id}$ , the Euclidean distance between their bounding box centers  $(d_{ij})$  and semantic relation  $(s_{ij})$ .

Real scenes may contain many objects (e.g., over 100), potentially forming a complete graph and resulting in a long scene description (over 32k symbols). This can degrade LLM performance due to the long context. However, retrieving a referred object typically doesn't require the location of all objects. Therefore, we propose a *deductive* scene reasoning algorithm to find objects efficiently.

The *deductive* scene reasoning algorithm involves several consecutive LLM calls. First, the LLM uses as input a scene description with object IDs  $O^{id}$  and their caption  $O^{caption}$ , along with the user's query query. It selects target and anchor objects IDs (TargetIds) and AnchorIds for answering the question in general case based on the objects semantics. The target object is the object that answers the user's query. The anchor object is the object with which the target object has spatial relations in the user's question (see example in Fig. 2). We create a scene description with additional location and connection details, but only for the selected Targets and Anchors. This results in a compact description focused on the objects relevant to the user's query in the special scene.

![](_page_3_Figure_7.jpeg)

Fig. 3. Qualitative examples of 3D open-vocabulary semantic segmentation on the Replica.

<span id="page-3-3"></span>TABLE I
3D OPEN-VOCABULARY SEMANTIC SEGMENTATION BENCHMARK.

|            |                                                          |                                  | Replica                          |                                  | ScanNet                             |                                     |                                     |  |  |
|------------|----------------------------------------------------------|----------------------------------|----------------------------------|----------------------------------|-------------------------------------|-------------------------------------|-------------------------------------|--|--|
|            | Methods                                                  | mAcc↑                            | mIoU↑                            | fmIoU↑                           | $mAcc \! \uparrow$                  | mIoU↑                               | fmIoU↑                              |  |  |
| Privileged | OpenFusion                                               | 0.41                             | 0.30                             | 0.58                             | 0.67                                | 0.53                                | 0.64                                |  |  |
| Zero-Shot  | ConceptFusion<br>OpenMask3D<br>ConceptGraphs<br>BBQ-CLIP | 0.29<br>-<br>0.36<br><b>0.38</b> | 0.11<br>-<br>0.18<br><b>0.27</b> | 0.14<br>-<br>0.15<br><b>0.48</b> | 0.49<br>0.34<br>0.52<br><b>0.56</b> | 0.26<br>0.18<br>0.26<br><b>0.34</b> | 0.31<br>0.20<br>0.29<br><b>0.36</b> |  |  |

For each object, we include a "relations" field in its description, listing sentences in the following template: "The  $o_i^{caption}$  with id  $o_i^{id}$  is  $s_{ij}$  and at distance  $d_{ij}$  m from the  $o_j^{caption}$  with id  $o_i^{id}$ ". To limit scene description length, we add edge  $e_{ij}$  to the scene graph only if  $o_i \in TargetObjects$  and  $o_j \in AnchorObjects$ . Using the compact scene description of relevant objects, the LLM retrieves the final objects in JSON format. If the response needs formatting, we make another LLM call to adjust it.

Algorithm 1 details our scene *deductive* inference algorithm. Results in Sec. IV-B demonstrate the benefits of incorporating spatial metric and semantic relations in the scene description and employing the *deductive* scene reasoning algorithm for object grounding using LLM.

### IV. EXPERIMENTS

<span id="page-3-1"></span>We conduct our experiments on Replica [76] and ScanNet [77] RGB-D data. For each datasets we select 8 scenes: (room0, room1, room2, office0, office1, office2, office3, office4) and (0011\_00, 0030\_00, 0046\_00, 0086\_00, 0222\_00, 0378\_00, 0389\_00, 0435\_00) respectively. We choose scenes for Replica to be in aligned with a previous researches. For the ScanNet, scenes were randomly selected based on least blur amount in RGB sequence. With the provided GT semantic segmentation annotation we perform 3D openvocabulary benchmarking with the closest related works (Sec. IV-A) to show advantage of BBQ 3D object-centric map scene representation. To examine the ability to answer complex queries that contain object relations we utilize ScanNet annotations from Sr3D+/Nr3D [62] and ScanRefer [61] datasets. The Sr3D+ dataset contains template-based references to objects based on their spatial relations with

TABLE II GRAPH EDGES ABLATION STUDY ON NR3D DATASET (GT OBJECTS).

| LLM       | Edge            | Recall@1<br>(Overall) | Recall@1 (View<br>Independent) | Recall@1 (View<br>Dependent) |
|-----------|-----------------|-----------------------|--------------------------------|------------------------------|
| Llama3-8B | -               | 36.1                  | 36.1                           | 36.0                         |
| Llama3-8B | Metric          | 43.8                  | 43.0                           | 46.3                         |
| Llama3-8B | Semantic        | 41.4                  | 37.8                           | 53.0                         |
| Llama3-8B | Metric+Semantic | 45.5                  | 43.3                           | 52.4                         |
| GPT-4o    | -               | 61.8                  | 67.8                           | 43.7                         |
| GPT-4o    | Metric          | 68.6                  | 73.9                           | 52.4                         |
| GPT-4o    | Semantic        | 50.5                  | 49.2                           | 54.9                         |
| GPT-4o    | Metric+Semantic | 68.4                  | 70.3                           | 62.1                         |

TABLE III GROUNDING ACCURACY ON SR3D+/NR3D DATASET.

<span id="page-4-2"></span>

|                    |         |      |                                                                          |      | Sr3D+ |      |           |      |             |      |  |
|--------------------|---------|------|--------------------------------------------------------------------------|------|-------|------|-----------|------|-------------|------|--|
| Methods            | Overall |      | Easy<br>A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 |      | Hard  |      | View Dep. |      | View Indep. |      |  |
| OpenFusion         | 12.6    | 2.4  | 14.0                                                                     | 2.4  | 1.3   | 1.3  | 3.8       | 2.5  | 13.7        | 2.4  |  |
| BBQ-CLIP           | 14.4    | 8.8  | 15.4                                                                     | 9.0  | 6.7   | 6.7  | 11.4      | 5.1  | 14.4        | 8.8  |  |
| ConceptGraphs 13.3 |         | 6.2  | 13.0                                                                     | 6.8  | 16.0  | 1.3  | 15.2      | 5.1  | 13.1        | 6.4  |  |
| BBQ                | 34.2    | 22.7 | 34.3                                                                     | 22.7 | 33.3  | 22.7 | 32.9      | 20.3 | 34.4        | 23.0 |  |

|                           | Overall |             |              | Easy        |             | Hard        |              | View Dep.                                                        |              | View Indep. |
|---------------------------|---------|-------------|--------------|-------------|-------------|-------------|--------------|------------------------------------------------------------------|--------------|-------------|
| Methods                   |         |             |              |             |             |             |              | A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 A@0.1 A@0.25 |              |             |
| OpenFusion                | 10.7    | 1.4         | 12.9         | 1.4         | 5.1         | 1.5         | 8.5          | 0.0                                                              | 11.4         | 1.9         |
| BBQ-CLIP                  | 15.3    | 9.4         | 18.1         | 11.0        | 8.1         | 5.6         | 8.1          | 6.1                                                              | 17.2         | 10.5        |
| ConceptGraphs 16.0<br>BBQ | 28.3    | 7.2<br>19.0 | 18.7<br>30.5 | 9.2<br>21.3 | 9.1<br>22.8 | 2.0<br>13.2 | 12.7<br>23.6 | 4.2<br>18.2                                                      | 17.0<br>29.8 | 8.1<br>19.3 |

other objects. The Nr3D and ScanRefer datasets contain various human-annotated natural language object references. For the template-based Sr3D+ dataset, we select all 661 unique queries with triplets of (target, relation, anchor) for the eight considered scenes from ScanNet. For the natural language Nr3D and ScanRefer datasets we select all queries from the eight considered scenes resulting in 699 and 720 queries respectively. Results are provided in Sec. [IV-B.](#page-4-0) All the experiments were conducted on a single Nvidia V100 with 32 GB of vRAM except for LLM where we use Nvidia H100 with 80 GB of vRAM.

### <span id="page-4-1"></span>*A. 3D open-vocabulary semantic segmentation*

To perform 3D open-vocabulary segmentation we extract CLIP features for each object cropped view. Our ablation between OpenCLIP [1], SigLip [5], and Eva2 [3] shows that the last model performs better in terms of quality by a large margin. We utilize Eva2 [78] and call this variant BBQ-CLIP.

*Evaluation protocol.* For all methods, we query only classes that exist on each scene inside the phrase *"an image of* <*class name*>*"* and calculate mAcc, mIoU, and frequency-weighted mIoU.

*Results.* As shown in Tab. [I,](#page-3-3) our BBQ-CLIP approach shows best results among other zero-shot algorithms (ConceptFusion [34], ConceptGraph [20], OpenMask3D [40]) in the 3D open-vocabulary segmentation and compeat with OpenFusion [36]. We position OpenFusion in a privileged group because the method exploits SEEM [8], which was trained on supervised segmentation tasks in evaluation domain.

### <span id="page-4-0"></span>*B. Scene graphs generation*

*Evaluation protocol.* During ablation experiments, we assess various methods for constructing a graph from ground-

TABLE IV GROUNDING ACCURACY ON SCANREFER DATASET.

<span id="page-4-3"></span>

| Methods      | A@0.25 | A@0.5 |  |
|--------------|--------|-------|--|
| LERF         | 4.4    | 0.3   |  |
| OpenScene    | 13.0   | 5.1   |  |
| LLM-Grounder | 17.1   | 5.3   |  |
| BBQ          | 19.4   | 11.6  |  |

truth point clouds of objects. We evaluate object grounding quality using the Recall@1 [20]. For experiments involving scene reconstruction, we use such metrics as Acc@0.1 [19], Acc@0.25 and Acc@0.5 [61]. A prediction is considered true positive if the Intersection over Union (IoU) between the selected object bounding box and the ground truth bounding box exceeds 0.1, 0.25 and 0.5, respectively.

*Results.* The Nr3D dataset annotates referring expressions as containing view-dependent and view-independent spatial relations. We conduct experiments on combining metric and semantic spatial edges to explore how the edge type affects the quality of object grounding for different types of queries. We use LLAMA3-8B [79] and GPT4-o [80] (*gpt4o-2024-08- 06*) in this study. For both models, adding semantic spatial edges improves the quality of object grounding compared to absence of edges and metric edges when the query contains view-dependent relations. Using a combination of metric and semantic spatial edges improves the quality for viewindependent queries compared to using only semantic spatial edges for both models, so we use this combination in further experiments.

Our approach surpasses existing open-vocabulary methods for 3D object grounding, notably outperforming Concept-Graphs [20], which also integrates an LLM, with scene text descriptions on Sr3D+ (Table [III\)](#page-4-2) and Nr3D (Table [III](#page-4-2) and Table [V\)](#page-5-1). In these experiments, we use the GPT4-o [80] (*gpt4o-2024-08-06*) for all methods. It is worth noting that our method outperforms baseline approaches for various types of queries, including different types of spatial relations (view dependent and view-independent), and mentions of color, shape. BBQ can process queries that do not mention target class explicitly, i.e. the object described by its function (Table [V\)](#page-5-1). Additionally, we compare our method with the baseline approaches LERF [43], OpenScene [41], LLM-Grounder [70] on the same ScanRefer subset used in the experiments in LLM-Grounder [70]. This subset consists of 14 ScanNet scenes and 998 referring expressions. Table [IV](#page-4-3) demonstrates the effectiveness of our approach compared to these baseline approaches.

Moreover, we demonstrate that leveraging an objectcentric textual description of a scene graph, interfaced via an LLM, significantly outperforms methods utilizing CLIP features for object grounding, such as OpenFusion [36] and our BBQ-CLIP. However, in some practical cases such approach can be usefull, especially if there are limited resources to call LLM.

TABLE V GROUNDING ACCURACY ON NR3D DATASET.

<span id="page-5-1"></span>

|               | Overall |        | w Spatial Lang. |        | w/o Spatial Lang. |        | w Color Lang. |        | w/o Color Lang. |        | w Shape Lang. |        | w/o Shape Lang. |        | w Target Mention |        |       | w/o Target Mention |
|---------------|---------|--------|-----------------|--------|-------------------|--------|---------------|--------|-----------------|--------|---------------|--------|-----------------|--------|------------------|--------|-------|--------------------|
| Methods       | A@0.1   | A@0.25 | A@0.1           | A@0.25 | A@0.1             | A@0.25 | A@0.1         | A@0.25 | A@0.1           | A@0.25 | A@0.1         | A@0.25 | A@0.1           | A@0.25 | A@0.1            | A@0.25 | A@0.1 | A@0.25             |
| OpenFusion    | 10.7    | 1.4    | 8.9             | 1.1    | 22.3              | 3.2    | 11.8          | 0.8    | 10.5            | 1.6    | 9.8           | 1.0    | 10.9            | 1.5    | 11.3             | 1.6    | 4.9   | 0.0                |
| BBQ-CLIP      | 15.3    | 9.4    | 14.7            | 8.8    | 19.1              | 13.8   | 24.4          | 16.8   | 13.4            | 7.9    | 12.7          | 6.9    | 15.7            | 9.9    | 16.3             | 10.0   | 4.9   | 3.3                |
| ConceptGraphs | 16.0    | 7.2    | 15.0            | 6.6    | 22.3              | 10.6   | 17.6          | 5.9    | 15.7            | 7.4    | 10.8          | 4.9    | 16.9            | 7.5    | 16.9             | 7.5    | 6.6   | 3.3                |
| BBQ           | 28.3    | 19.0   | 28.1            | 19.2   | 29.8              | 18.1   | 25.2          | 17.6   | 29.0            | 19.3   | 34.3          | 23.5   | 27.3            | 18.3   | 29.6             | 19.7   | 14.8  | 11.5               |

![](_page_5_Picture_2.jpeg)

Fig. 4. Qualitative examples of 3D referred object grounding on the Sr3D+/Nr3D datasets.

# <span id="page-5-0"></span>*C. Real-World Experiments*

BBQ was tested using custom SensorBox hardware (Fig. [5\)](#page-5-2). The SensorBox contains the following sensors: one stereo RGB Zed X camera with integrated IMUs, two LiDARs and two fisheye RGB cameras. The SensorBox is constructed on a rigid metal frame with a built-in LiPo battery and an on-board PC Zotac (11th Gen i7-11800H @2.3 GHz, Nvidia GeForce RTX3080 16GB Mobile, 62.5 GB RAM), thereby ensuring the real-time data acquisition.

First, we measured BBQ mapping performance on our hardware with publicly available data. Because performance relies on the number of objects, we chose room0 RGB-D sequence with stride 10 from the Replica dataset for benchmarking. As demonstrated in Fig. [6,](#page-5-3) BBQ works on the on-board Zotac PC with considerable mean time of 1.18 s/it and an overall time of 7 min 52 seconds for scene. It is almost ×3 faster than ConceptGraphs [20].

Second, we conducted experiments on real-world data in our facilities. We equipped a mobile platform, Husky, with the SensorBox (Fig. [5\)](#page-5-2) and performed whole pipeline testing. We reconstructed pose with vSLAM [81] and generate depth images with the neural network [82]. The 3D mapping process was launched onboard, but vLLM and LLM were deployed on server with an Nvidia V100 32Gb vRAM with API. The success of the performed experiments demonstrated BBQ's ability to be deployed in a real-life scenario. We have added examples of our algorithm running on real data to the supplementary materials.

# V. LIMITATIONS

It should be noted that BBQ works under the assumption of a static environment equivalent to a standard indoor room. To handle dynamic, existing tracking methods [28], [83], [84] should be applied. For large and complex form locations, 3D scene graph in current implementation may not reflect semantic spatial relations correctly.

Also, conducted experiments highlight that our 3D objectcentric map construction method is limited in its ability to

![](_page_5_Picture_11.jpeg)

![](_page_5_Figure_12.jpeg)

![](_page_5_Figure_13.jpeg)

<span id="page-5-2"></span>Fig. 5. Husky mobile robot with SensorBox used for real-world experiments

<span id="page-5-3"></span>Fig. 6. 3D mapping process speed on the Zotac on-board computer with Replica room0 RGB-D sequence

successfully distinguish tiny objects in the image. It is a general problem of visual foundation models, which can be partially solved with an integration of target-specific detectors [85] or with more scene exploration where the camera is placed closer to objects of interest to successfully map such instances.

## VI. CONCLUSION

With BBQ, we advance the limits of 3D scene perception by integrating language models with general world knowledge and our scene-specific graph representation. The successful outcomes of our experiments on the complex Nr3D, Sr3D, and ScanRefer datasets, as well as on real-life data, demonstrate the effectiveness of our approach with metric and semantic scene edges, opening new avenues for a more comprehensive and flexible understanding and interaction with 3D scenes. We hope that our resource-efficient code implementation will facilitate BBQ applications in real-world robotics projects that bridge the communication gap between humans and intelligent autonomous agents.

# ACKNOWLEDGMENT

We thank team of Sberbank Robotics Center for supporting us in conducting real-world robotic experiments.

## REFERENCES

- [1] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, *et al.*, "Learning transferable visual models from natural language supervision," in *International conference on machine learning*. PMLR, 2021, pp. 8748–8763.
- [2] N. Mu, A. Kirillov, D. Wagner, and S. Xie, "Slip: Self-supervision meets language-image pre-training," in *European conference on computer vision*. Springer, 2022, pp. 529–544.
- [3] Y. Fang, Q. Sun, X. Wang, T. Huang, X. Wang, and Y. Cao, "Eva-02: A visual representation for neon genesis," *arXiv preprint arXiv:2303.11331*, 2023.
- [4] Q. Sun, J. Wang, Q. Yu, Y. Cui, F. Zhang, X. Zhang, and X. Wang, "Eva-clip-18b: Scaling clip to 18 billion parameters," *arXiv preprint arXiv:2402.04252*, 2024.
- [5] X. Zhai, B. Mustafa, A. Kolesnikov, and L. Beyer, "Sigmoid loss for language image pre-training," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 11 975– 11 986.
- [6] Z. Sun, Y. Fang, T. Wu, P. Zhang, Y. Zang, S. Kong, Y. Xiong, D. Lin, and J. Wang, "Alpha-clip: A clip model focusing on wherever you want," *arXiv preprint arXiv:2312.03818*, 2023.
- [7] A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W.-Y. Lo, *et al.*, "Segment anything," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 4015–4026.
- [8] X. Zou, J. Yang, H. Zhang, F. Li, L. Li, J. Wang, L. Wang, J. Gao, and Y. J. Lee, "Segment everything everywhere all at once," *Advances in Neural Information Processing Systems*, vol. 36, 2024.
- [9] H. Liu, C. Li, Q. Wu, and Y. J. Lee, "Visual instruction tuning," 2023.
- [10] R. Girdhar, A. El-Nouby, Z. Liu, M. Singh, K. V. Alwala, A. Joulin, and I. Misra, "Imagebind: One embedding space to bind them all," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 15 180–15 190.
- [11] J. Li, D. Li, S. Savarese, and S. Hoi, "Blip-2: Bootstrapping languageimage pre-training with frozen image encoders and large language models," in *International conference on machine learning*. PMLR, 2023, pp. 19 730–19 742.
- [12] M. Ranzinger, G. Heinrich, J. Kautz, and P. Molchanov, "Am-radio: Agglomerative model–reduce all domains into one," *arXiv preprint arXiv:2312.06709*, 2023.
- [13] S.-C. Wu, K. Tateno, N. Navab, and F. Tombari, "Incremental 3d semantic scene graph prediction from rgb sequences," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 5064–5074.
- [14] M. Tsimpoukelli, J. L. Menick, S. Cabi, S. Eslami, O. Vinyals, and F. Hill, "Multimodal few-shot learning with frozen language models," *Advances in Neural Information Processing Systems*, vol. 34, pp. 200– 212, 2021.
- [15] H. Liu, C. Li, Y. Li, and Y. J. Lee, "Improved baselines with visual instruction tuning," 2023.
- [16] H. Liu, C. Li, Y. Li, B. Li, Y. Zhang, S. Shen, and Y. J. Lee, "Llava-next: Improved reasoning, ocr, and world knowledge," January 2024. [Online]. Available: [https://llava-vl.github.io/blog/](https://llava-vl.github.io/blog/2024-01-30-llava-next/) [2024-01-30-llava-next/](https://llava-vl.github.io/blog/2024-01-30-llava-next/)
- [17] I. Armeni, Z.-Y. He, J. Gwak, A. R. Zamir, M. Fischer, J. Malik, and S. Savarese, "3d scene graph: A structure for unified semantics, 3d space, and camera," in *Proceedings of the IEEE/CVF international conference on computer vision*, 2019, pp. 5664–5673.
- [18] S. Koch, N. Vaskevicius, M. Colosi, P. Hermosilla, and T. Ropinski, "Open3dsg: Open-vocabulary 3d scene graphs from point clouds with queryable objects and open-set relationships," *arXiv preprint arXiv:2402.12259*, 2024.
- [19] A. Werby, C. Huang, M. Buchner, A. Valada, and W. Burgard, ¨ "Hierarchical open-vocabulary 3d scene graphs for language-grounded robot navigation," in *First Workshop on Vision-Language Models for Navigation and Manipulation at ICRA 2024*, 2024.
- [20] Q. Gu, A. Kuwajerwala, S. Morin, K. M. Jatavallabhula, B. Sen, A. Agarwal, C. Rivera, W. Paul, K. Ellis, R. Chellappa, *et al.*, "Conceptgraphs: Open-vocabulary 3d scene graphs for perception and planning," in *2024 IEEE International Conference on Robotics and Automation (ICRA)*, 2024.
- [21] W. Chen, S. Hu, R. Talak, and L. Carlone, "Leveraging large language models for robot 3d scene understanding," *arXiv preprint arXiv:2209.05629*, 2022.

- [22] K. Kim, K. Yoon, J. Jeon, Y. In, J. Moon, D. Kim, and C. Park, "Llm4sgg: Large language model for weakly supervised scene graph generation," *arXiv e-prints*, pp. arXiv–2310, 2023.
- [23] Y. Hong, H. Zhen, P. Chen, S. Zheng, Y. Du, Z. Chen, and C. Gan, "3d-llm: Injecting the 3d world into large language models," *Advances in Neural Information Processing Systems*, vol. 36, pp. 20 482–20 494, 2023.
- [24] H. Huang, Z. Wang, R. Huang, L. Liu, X. Cheng, Y. Zhao, T. Jin, and Z. Zhao, "Chat-3d v2: Bridging 3d scene and large language models with object identifiers," *arXiv preprint arXiv:2312.08168*, 2023.
- [25] R. Fu, J. Liu, X. Chen, Y. Nie, and W. Xiong, "Scene-llm: Extending language model for 3d visual understanding and reasoning," *arXiv preprint arXiv:2403.11401*, 2024.
- [26] S. Huang, L. Dong, W. Wang, Y. Hao, S. Singhal, S. Ma, T. Lv, L. Cui, O. K. Mohammed, B. Patra, *et al.*, "Language is not all you need: Aligning perception with language models," *Advances in Neural Information Processing Systems*, vol. 36, 2024.
- [27] M. E. Banani, A. Raj, K.-K. Maninis, A. Kar, Y. Li, M. Rubinstein, D. Sun, L. Guibas, J. Johnson, and V. Jampani, "Probing the 3d awareness of visual foundation models," *arXiv preprint arXiv:2404.08636*, 2024.
- [28] N. Tumanyan, A. Singer, S. Bagon, and T. Dekel, "Dino-tracker: Taming dino for self-supervised point tracking in a single video," *arXiv preprint arXiv:2403.14548*, 2024.
- [29] N. Keetha, A. Mishra, J. Karhade, K. M. Jatavallabhula, S. Scherer, M. Krishna, and S. Garg, "Anyloc: Towards universal visual place recognition," *IEEE Robotics and Automation Letters*, 2023.
- [30] S. Amir, Y. Gandelsman, S. Bagon, and T. Dekel, "Deep vit features as dense visual descriptors," *arXiv preprint arXiv:2112.05814*, vol. 2, no. 3, p. 4, 2021.
- [31] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, *et al.*, "Chain-of-thought prompting elicits reasoning in large language models," *Advances in neural information processing systems*, vol. 35, pp. 24 824–24 837, 2022.
- [32] N. Tsagkas, O. Mac Aodha, and C. X. Lu, "Vl-fields: Towards language-grounded neural implicit spatial representations," *arXiv preprint arXiv:2305.12427*, 2023.
- [33] H. Ha and S. Song, "Semantic abstraction: Open-world 3d scene understanding from 2d vision-language models," *arXiv preprint arXiv:2207.11514*, 2022.
- [34] K. Jatavallabhula, A. Kuwajerwala, Q. Gu, M. Omama, T. Chen, S. Li, G. Iyer, S. Saryazdi, N. Keetha, A. Tewari, J. Tenenbaum, C. de Melo, M. Krishna, L. Paull, F. Shkurti, and A. Torralba, "Conceptfusion: Open-set multimodal 3d mapping," *Robotics: Science and Systems (RSS)*, 2023.
- [35] S. Lu, H. Chang, E. P. Jing, A. Boularias, and K. Bekris, "Ovir-3d: Open-vocabulary 3d instance retrieval without training on 3d data," in *Conference on Robot Learning*. PMLR, 2023, pp. 1610–1620.
- [36] K. Yamazaki, T. Hanyu, K. Vo, T. Pham, M. Tran, G. Doretto, A. Nguyen, and N. Le, "Open-fusion: Real-time open-vocabulary 3d mapping and queryable scene representation," *arXiv preprint arXiv:2310.03923*, 2023.
- [37] Z. Huang, X. Wu, X. Chen, H. Zhao, L. Zhu, and J. Lasenby, "Openins3d: Snap and lookup for 3d open-vocabulary instance segmentation," *arXiv preprint arXiv:2309.00616*, 2023.
- [38] P. D. Nguyen, T. D. Ngo, C. Gan, E. Kalogerakis, A. Tran, C. Pham, and K. Nguyen, "Open3dis: Open-vocabulary 3d instance segmentation with 2d mask guidance," *arXiv preprint arXiv:2312.10671*, 2023.
- [39] J. Yang, R. Ding, W. Deng, Z. Wang, and X. Qi, "Regionplc: Regional point-language contrastive learning for open-world 3d scene understanding," *arXiv preprint arXiv:2304.00962*, 2023.
- [40] A. Takmaz, E. Fedele, R. W. Sumner, M. Pollefeys, F. Tombari, and F. Engelmann, "Openmask3d: Open-vocabulary 3d instance segmentation," *arXiv preprint arXiv:2306.13631*, 2023.
- [41] S. Peng, K. Genova, C. Jiang, A. Tagliasacchi, M. Pollefeys, T. Funkhouser, *et al.*, "Openscene: 3d scene understanding with open vocabularies," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 815–824.
- [42] Y. Yin, Y. Liu, Y. Xiao, D. Cohen-Or, J. Huang, and B. Chen, "Sai3d: Segment any instance in 3d scenes," *arXiv preprint arXiv:2312.11557*, 2023.
- [43] J. Kerr, C. M. Kim, K. Goldberg, A. Kanazawa, and M. Tancik, "Lerf: Language embedded radiance fields," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 19 729–19 739.

- [44] K. Liu, F. Zhan, J. Zhang, M. Xu, Y. Yu, A. El Saddik, C. Theobalt, E. Xing, and S. Lu, "Weakly supervised 3d open-vocabulary segmentation," *Advances in Neural Information Processing Systems*, vol. 36, pp. 53 433–53 456, 2023.
- [45] G. Liao, K. Zhou, Z. Bao, K. Liu, and Q. Li, "Ov-nerf: Openvocabulary neural radiance fields with vision and language foundation models for 3d semantic understanding," *arXiv preprint arXiv:2402.04648*, 2024.
- [46] M. Tie, J. Wei, Z. Wang, K. Wu, S. Yuan, K. Zhang, J. Jia, J. Zhao, Z. Gan, and W. Ding, "O2v-mapping: Online openvocabulary mapping with neural implicit representation," *arXiv preprint arXiv:2404.06836*, 2024.
- [47] H. Ying, Y. Yin, J. Zhang, F. Wang, T. Yu, R. Huang, and L. Fang, "Omniseg3d: Omniversal 3d segmentation via hierarchical contrastive learning," *arXiv preprint arXiv:2311.11666*, 2023.
- [48] J.-C. Shi, M. Wang, H.-B. Duan, and S.-H. Guan, "Language embedded 3d gaussians for open-vocabulary scene understanding," *arXiv preprint arXiv:2311.18482*, 2023.
- [49] M. Qin, W. Li, J. Zhou, H. Wang, and H. Pfister, "Langsplat: 3d language gaussian splatting," *arXiv preprint arXiv:2312.16084*, 2023.
- [50] S. Jiang, *Feature 3DGS: Supercharging 3D Gaussian Splatting to Enable Distilled Feature Fields*. University of California, Los Angeles, 2023.
- [51] H. Guo, H. Zhu, S. Peng, Y. Wang, Y. Shen, R. Hu, and X. Zhou, "Sam-guided graph cut for 3d instance segmentation," *arXiv preprint arXiv:2312.08372*, 2023.
- [52] X. Zhu, H. Zhou, P. Xing, L. Zhao, H. Xu, J. Liang, A. Hauptmann, T. Liu, and A. Gallagher, "Open-vocabulary 3d semantic segmentation with text-to-image diffusion models," *arXiv preprint arXiv:2407.13642*, 2024.
- [53] N. Hughes, Y. Chang, and L. Carlone, "Hydra: A real-time spatial perception system for 3d scene graph construction and optimization," *arXiv preprint arXiv:2201.13360*, 2022.
- [54] U.-H. Kim, J.-M. Park, T.-J. Song, and J.-H. Kim, "3-d scene graph: A sparse and semantic representation of physical environments for intelligent agents," *IEEE transactions on cybernetics*, vol. 50, no. 12, pp. 4921–4933, 2019.
- [55] Z. Wang, B. Cheng, L. Zhao, D. Xu, Y. Tang, and L. Sheng, "Vlsat: visual-linguistic semantics assisted training for 3d semantic scene graph prediction in point cloud," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 21 560–21 569.
- [56] C. Zhang, X. Yang, J. Hou, K. Kitani, W. Cai, and F.-J. Chu, "Egosg: Learning 3d scene graphs from egocentric rgb-d sequences," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 2535–2545.
- [57] L. Chen, X. Wang, J. Lu, S. Lin, C. Wang, and G. He, "Clipdriven open-vocabulary 3d scene graph generation via cross-modality contrastive learning," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 27 863–27 873.
- [58] J. Wald, H. Dhamo, N. Navab, and F. Tombari, "Learning 3d semantic scene graphs from 3d indoor reconstructions," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2020, pp. 3961–3970.
- [59] J. Wald, N. Navab, and F. Tombari, "Learning 3d semantic scene graphs with instance embeddings," *International Journal of Computer Vision*, vol. 130, no. 3, pp. 630–651, 2022.
- [60] D. Honerkamp, M. Buchner, F. Despinoy, T. Welschehold, and A. Val- ¨ ada, "Language-grounded dynamic scene graphs for interactive object search with mobile manipulation," *IEEE Robotics and Automation Letters*, 2024.
- [61] D. Z. Chen, A. X. Chang, and M. Nießner, "Scanrefer: 3d object localization in rgb-d scans using natural language," in *European conference on computer vision*. Springer, 2020, pp. 202–221.
- [62] P. Achlioptas, A. Abdelreheem, F. Xia, M. Elhoseiny, and L. J. Guibas, "ReferIt3D: Neural listeners for fine-grained 3d object identification in real-world scenes," in *16th European Conference on Computer Vision (ECCV)*, 2020.
- [63] A. Majumdar, A. Ajay, X. Zhang, P. Putta, S. Yenamandra, M. Henaff, S. Silwal, P. Mcvay, O. Maksymets, S. Arnaud, *et al.*, "Openeqa: Embodied question answering in the era of foundation models," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 16 488–16 498.
- [64] C. Zhu, T. Wang, W. Zhang, K. Chen, and X. Liu, "Empower-

- ing 3d visual grounding with reasoning capabilities," *arXiv preprint arXiv:2407.01525*, 2024.
- [65] Y. Li, Z. Wang, and W. Liang, "R2g: Reasoning to ground in 3d scenes," *arXiv preprint arXiv:2408.13499*, 2024.
- [66] Y. Zhang, Z. Gong, and A. X. Chang, "Multi3drefer: Grounding text description to multiple 3d objects," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2023, pp. 15 225– 15 236.
- [67] L. Zhao, D. Cai, L. Sheng, and D. Xu, "3dvg-transformer: Relation modeling for visual grounding on point clouds," in *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 2021, pp. 2928–2937.
- [68] J. Hsu, J. Mao, and J. Wu, "Ns3d: Neuro-symbolic grounding of 3d objects and relations," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2023, pp. 2614–2623.
- [69] Z. Yuan, J. Ren, C.-M. Feng, H. Zhao, S. Cui, and Z. Li, "Visual programming for zero-shot open-vocabulary 3d visual grounding," in *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, 2024, pp. 20 623–20 633.
- [70] J. Yang, X. Chen, S. Qian, N. Madaan, M. Iyengar, D. F. Fouhey, and J. Chai, "Llm-grounder: Open-vocabulary 3d visual grounding with large language model as an agent," in *2024 IEEE International Conference on Robotics and Automation (ICRA)*. IEEE, 2024, pp. 7694–7701.
- [71] S. Chen, P.-L. Guhur, M. Tapaswi, C. Schmid, and I. Laptev, "Language conditioned spatial relation reasoning for 3d object grounding," *Advances in neural information processing systems*, vol. 35, pp. 20 522–20 535, 2022.
- [72] Y. Chen, S. Yang, H. Huang, T. Wang, R. Lyu, R. Xu, D. Lin, and J. Pang, "Grounded 3d-llm with referent tokens," *arXiv preprint arXiv:2405.10370*, 2024.
- [73] T. Miyanishi, D. Azuma, S. Kurita, and M. Kawanabe, "Cross3dvg: Cross-dataset 3d visual grounding on different rgb-d scans," in *2024 International Conference on 3D Vision (3DV)*. IEEE, 2024, pp. 717– 727.
- [74] C. Zhang, D. Han, S. Zheng, J. Choi, T.-H. Kim, and C. S. Hong, "Mobilesamv2: Faster segment anything to everything," *arXiv preprint arXiv:2312.09579*, 2023.
- [75] T. Darcet, M. Oquab, J. Mairal, and P. Bojanowski, "Vision transformers need registers," *arXiv preprint arXiv:2309.16588*, 2023.
- [76] J. Straub, T. Whelan, L. Ma, Y. Chen, E. Wijmans, S. Green, J. J. Engel, R. Mur-Artal, C. Ren, S. Verma, *et al.*, "The replica dataset: A digital replica of indoor spaces," *arXiv preprint arXiv:1906.05797*, 2019.
- [77] A. Dai, A. X. Chang, M. Savva, M. Halber, T. Funkhouser, and M. Nießner, "Scannet: Richly-annotated 3d reconstructions of indoor scenes," in *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2017, pp. 5828–5839.
- [78] L. Yang, Y. Wang, X. Li, X. Wang, and J. Yang, "Fine-grained visual prompting," *Advances in Neural Information Processing Systems*, vol. 36, 2024.
- [79] AI@Meta, "Llama 3 model card," 2024. [Online]. Available: [https://github.com/meta-llama/llama3/blob/main/MODEL](https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md) CARD.md
- [80] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, *et al.*, "Gpt-4 technical report," *arXiv preprint arXiv:2303.08774*, 2023.
- [81] C. Campos, R. Elvira, J. J. G. Rodr´ıguez, J. M. Montiel, and J. D. Tardos, "Orb-slam3: An accurate open-source library for visual, ´ visual–inertial, and multimap slam," *IEEE Transactions on Robotics*, vol. 37, no. 6, pp. 1874–1890, 2021.
- [82] J. Li, P. Wang, P. Xiong, T. Cai, Z. Yan, L. Yang, J. Liu, H. Fan, and S. Liu, "Practical stereo matching via cascaded recurrent network with adaptive correlation," in *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, 2022, pp. 16 263–16 272.
- [83] N. Karaev, I. Rocco, B. Graham, N. Neverova, A. Vedaldi, and C. Rupprecht, "Cotracker: It is better to track together," in *European Conference on Computer Vision*. Springer, 2024, pp. 18–35.
- [84] V. Stanojevic and B. Todorovi ´ c, "Boosttrack++: using tracklet informa- ´ tion to detect more objects in multiple object tracking," *arXiv preprint arXiv:2408.13003*, 2024.
- [85] M. Muzammul and X. Li, "Comprehensive review of deep learningbased tiny object detection: challenges, strategies, and future directions," *Knowledge and Information Systems*, pp. 1–89, 2025.