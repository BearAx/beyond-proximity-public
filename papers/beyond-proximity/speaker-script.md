# Speaker Script: Beyond Proximity

*(Note: This script is designed to sound natural, enthusiastic, and slightly improvised. Pause at the commas and ellipses to let the points land.)*

## Slide 1: Title Slide
"Alright, hey everyone. Thanks for coming. Today I’m going to share some work we’ve been doing on 3D scene understanding. The project is called 'Beyond Proximity,' and it’s basically about how we can take these amazing 3D Gaussian Splatting environments and actually teach a system to *understand* what it's looking at—not just render it. So, let's dive in."

## Slide 2: The Core Problem
"So, we all know 3D Gaussian Splatting is incredible, right? It gives us these beautiful, photorealistic, real-time renders. But there's a catch. Under the hood, the system is kind of... dumb. It’s just geometric and photometric points in space. It doesn't know that a cluster of points is a 'chair' or a 'stage.' And if we ever want to use these environments for real robotics, or VR, or just natural language querying, the system fundamentally needs a semantic structure. It has to understand the space."

## Slide 3: Existing Approaches & Their Flaws
"Now, people have obviously tried to solve this. The usual go-to is either feature distillation—like LERF—where you bake VLM features directly into the 3D space. And that’s cool for simple keyword searches, but it totally smooths out object boundaries and completely fails at complex compositional reasoning. On the flip side, you have explicit 3D segmentation, like ConceptGraphs. But lifting 2D segments into a 3D graph scales horribly for open-vocabulary tasks, and it really struggles to figure out high-level architecture. Like, it doesn't know what a 'room' is."

## Slide 4: The Hierarchy Construction Dilemma
"And speaking of rooms... building a hierarchy of a scene is notoriously hard. If you look at how systems try to group things today, they rely on one of two extremes. If you use pure geometry—just camera distance—it arbitrarily splits up large rooms. Like, it'll think the stage of a ballroom and the back row of the audience are two different rooms just because the cameras are far apart. But if you use pure semantics—just what things look like—it hallucinates. It’ll merge a lobby and a distant hallway into one zone just because they have the same carpet. Both approaches fail."

## Slide 5: Our Insight
"So our insight was... what if we stop trying to force semantics into 3D primitives? What if we just step back, treat 3DGS as what it is—a flawless rendering engine—and just generate noise-free 2D views? We can then just unleash state-of-the-art 2D Vision-Language Models directly onto those renders. It's a rendering-first paradigm."

## Slide 6: The Two-Pass Solution
"To actually build the hierarchy without the geometry-versus-semantics dilemma, we built a Two-Pass Clustering algorithm. Pass one is the geometric proximity graph. We use adaptive thresholds on camera distance to form really conservative clusters. This stops the system from hallucinating and merging distant rooms. Then, we hit it with a Semantic Merge pass. We have the VLM explicitly extract architectural metadata—like what direction the camera is facing, and what major landmarks are visible. This lets us confidently stitch those geometrically distant clusters back together if they share the same physical space. So, the stage-facing cameras and audience-facing cameras get merged perfectly."

## Slide 7: Querying the Scene
"Once we have this beautiful tree, querying it is super elegant. You just type in plain English—like 'Find the fire extinguisher near the exit'—and an LLM breaks that down. It traverses our semantic tree top-down. And because we summarize every node in like 10 to 15 words, the LLM can instantly prune out irrelevant rooms without processing heavy images. It's incredibly token-efficient."

## Slide 8: The Localization Problem
"But here was the crazy thing we ran into. We could navigate the tree perfectly to find the right views... but standard VLMs are honestly pretty terrible at drawing bounding boxes. They can tell you the fire extinguisher is there, but the box will be misaligned by like 10 to 20 percent. For small objects, that’s basically useless."

## Slide 9: Crop-and-Requery
"So we fixed this with a Two-Stage Refinement pipeline. Stage one forces the VLM to use a spatial Chain-of-Thought—literally breaking the image into grid thirds in its head to get a rough box. But we don't stop there. Stage two is 'Crop-and-Requery.' If we get a hit, we aggressively crop the high-res original image around that rough box, and feed *that* zoomed-in crop back to the VLM. It refines the box, and then we just map the coordinates back to the original image."

## Slide 10: Results - Topology
"The results are honestly exactly what we hoped for. On a really challenging, interconnected Conference Hall scene, our Two-Pass clustering achieved 100% room-level topological accuracy. The pure geometric baseline fractured the ballroom, the pure semantic baseline merged the lobby with the back corridor... but our hybrid approach nailed it. It perfectly isolated the rooms while keeping the big spaces intact."

## Slide 11: Results - Localization
"And for the bounding boxes? The Crop-and-Requery pipeline blew the standard single-pass VLM out of the water. Over 50 challenging 'find' queries, we saw a 34% improvement in Intersection-over-Union. The bounding boxes were suddenly locking tightly to the actual pixel boundaries of the objects. We also implemented a scoring system so if an object is seen from five different cameras, the system automatically surfaces the highest-confidence, most centralized 'best view'."

## Slide 12: Conclusion & Future Work
"So to wrap up... we really believe that off-the-shelf 2D VLMs can drive incredibly precise 3D scene reasoning, without needing complex 3D feature distillation. You just have to structure the clustering and querying pipelines correctly. For next steps, we're looking at taking these highly refined 2D bounding boxes and using the 3DGS depth maps to unproject them into exact 3D world coordinates. We're also looking at automated camera placement so nobody even has to manually capture the scene. Thanks so much for listening, I'd love to take any questions."