<!--
STALE — do not use for the article sprint. Overclaims on results slides.
Source of truth: papers/beyond-proximity/main.tex
-->
---
theme: seriph
background: https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=2070&auto=format&fit=crop
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  SemanticSplat: Graph-Pruned Semantic Search
drawings:
  persist: false
transition: slide-up
css: unocss
title: SemanticSplat: Graph-Pruned Semantic Search
---

# SemanticSplat: Graph-Pruned Semantic Search

Two-Pass Geometric-Semantic Clustering for Hierarchical 3D Scene Understanding

<div class="pt-12">
  <span @click="$slidev.nav.next" class="px-4 py-2 rounded-full cursor-pointer bg-white bg-opacity-10 hover:bg-opacity-20 transition-all">
    A Rendering-First Paradigm for 3D Gaussian Splatting <carbon-arrow-right class="inline"/>
  </span>
</div>

---
layout: default
---

# 3DGS is Beautiful, But "Dumb"

<div class="grid grid-cols-2 gap-8 mt-10">
  <div>
    <ul class="space-y-4">
      <li v-click><carbon-image class="inline mr-2 text-blue-500"/><strong>Photorealistic</strong> real-time rendering.</li>
      <li v-click><carbon-cube class="inline mr-2 text-green-500"/>Purely <strong>geometric and photometric</strong> (point clouds).</li>
      <li v-click class="text-red-500"><carbon-warning class="inline mr-2"/><strong>The Missing Link:</strong> No semantic structure.</li>
    </ul>
  </div>
  <div v-click>
    <div class="p-6 bg-gray-100 dark:bg-gray-800 rounded-lg border-l-4 border-blue-500 shadow-lg mt-4 transform hover:scale-105 transition-all">
      <h3 class="!m-0 !mb-2 flex items-center gap-2"><carbon-help class="text-blue-500"/> Why it matters</h3>
      <p class="!m-0 text-sm opacity-80 leading-relaxed">Downstream tasks like robotics, VR, and natural language querying require the system to <em>understand</em> what it's looking at, not just render it.</p>
    </div>
  </div>
</div>

---
layout: two-cols
---

# Existing Approaches...
And their flaws.

::right::

<div class="mt-14 ml-8">
  <v-clicks>
    <div class="mb-8 p-4 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm">
      <div class="flex items-center gap-2 text-xl mb-2 text-blue-500 font-bold">
        <carbon-analytics /> Feature Distillation (e.g., LERF)
      </div>
      <div class="text-sm opacity-80 mb-3">Embeds VLM features into 3D. Good for point-wise keyword search.</div>
      <div class="text-sm text-red-700 dark:text-red-300 bg-red-100 dark:bg-red-900/30 p-2 rounded">
        <strong>Flaw:</strong> Smooths out boundaries, lacks compositional reasoning.
      </div>
    </div>
    <div class="p-4 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm">
      <div class="flex items-center gap-2 text-xl mb-2 text-green-500 font-bold">
        <carbon-category /> Explicit 3D Segmentation (e.g., ConceptGraphs)
      </div>
      <div class="text-sm opacity-80 mb-3">Lifts 2D segments to 3D graphs.</div>
      <div class="text-sm text-red-700 dark:text-red-300 bg-red-100 dark:bg-red-900/30 p-2 rounded">
        <strong>Flaw:</strong> Scales poorly to open-vocabulary, struggles with high-level architectural hierarchy.
      </div>
    </div>
  </v-clicks>
</div>

---
layout: center
class: text-center
---

# The Hierarchy Construction Dilemma
<div class="text-2xl mt-4 opacity-80 font-serif italic">Pure Geometry vs. Pure Semantics</div>

<div class="grid grid-cols-2 gap-8 mt-12 text-left">
  <div v-click class="p-6 border border-gray-300 dark:border-gray-700 rounded-xl shadow-lg relative overflow-hidden bg-white dark:bg-[#121212]">
    <div class="absolute -top-4 -right-4 p-4 opacity-10"><carbon-cube class="text-9xl text-blue-500"/></div>
    <h3 class="text-blue-500 flex items-center gap-2 font-bold"><carbon-rule/> Pure Geometry</h3>
    <p class="opacity-80 font-semibold mt-2">Splits contiguous spaces.</p>
    <p class="text-sm bg-blue-500/10 p-3 rounded mt-4 italic">Example: A ballroom stage and its audience get separated because the cameras are physically far apart.</p>
  </div>
  <div v-click class="p-6 border border-gray-300 dark:border-gray-700 rounded-xl shadow-lg relative overflow-hidden bg-white dark:bg-[#121212]">
    <div class="absolute -top-4 -right-4 p-4 opacity-10"><carbon-color-palette class="text-9xl text-green-500"/></div>
    <h3 class="text-green-500 flex items-center gap-2 font-bold"><carbon-color-palette/> Pure Semantics</h3>
    <p class="opacity-80 font-semibold mt-2">Merges disconnected spaces.</p>
    <p class="text-sm bg-green-500/10 p-3 rounded mt-4 italic">Example: A lobby and a distant corridor get merged because they share the same carpet and lighting.</p>
  </div>
</div>

---
layout: image-right
image: /images/rendered-image.png
backgroundSize: cover
---

# Our Insight
<h3 class="text-gray-400 font-serif italic">The Rendering-First Paradigm</h3>

<v-clicks class="mt-8 space-y-6">
  <div class="flex items-start gap-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm">
    <div class="bg-red-100 dark:bg-red-900/30 p-2 rounded-full"><carbon-close-outline class="text-red-500 text-xl"/></div>
    <div class="pt-1">Stop forcing semantics into 3D primitives.</div>
  </div>
  <div class="flex items-start gap-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm">
    <div class="bg-blue-100 dark:bg-blue-900/30 p-2 rounded-full"><carbon-video class="text-blue-500 text-xl"/></div>
    <div class="pt-1">Treat 3DGS as an ideal <strong>rendering engine</strong>.</div>
  </div>
  <div class="flex items-start gap-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm">
    <div class="bg-green-100 dark:bg-green-900/30 p-2 rounded-full"><carbon-image class="text-green-500 text-xl"/></div>
    <div class="pt-1">Generate noise-free, perfect 2D viewpoints.</div>
  </div>
  <div class="flex items-start gap-4 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg shadow-sm">
    <div class="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-full"><carbon-machine-learning-model class="text-purple-500 text-xl"/></div>
    <div class="pt-1 leading-snug">Leverage state-of-the-art <strong>2D Vision-Language Models (VLMs)</strong> directly on the renders.</div>
  </div>
</v-clicks>

---
layout: default
---

# Two-Pass Geometric-Semantic Clustering
<p class="opacity-60 mb-8 font-serif italic">The Core Solution</p>

<div class="grid grid-cols-2 gap-8">
  <div v-click class="bg-gray-50 dark:bg-[#1a1a1a] p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-xl relative mt-4">
    <div class="text-2xl absolute -top-5 left-6 bg-blue-500 text-white w-10 h-10 flex items-center justify-center rounded-lg shadow-lg font-bold">1</div>
    <h3 class="text-xl mb-4 mt-2 text-blue-500 font-bold border-b border-blue-100 dark:border-blue-900 pb-2">Geometric Proximity Graph</h3>
    <ul class="space-y-3 opacity-90 text-sm">
      <li class="flex items-start gap-2"><carbon-chart-scatter class="text-blue-400 mt-1 flex-shrink-0"/>Adaptive thresholding based on camera distance.</li>
      <li class="flex items-start gap-2"><carbon-checkmark class="text-green-400 mt-1 flex-shrink-0"/>Prevents cross-room hallucinations.</li>
    </ul>
    <div class="mt-4 text-xs text-center text-gray-500 dark:text-gray-400 uppercase tracking-wider bg-gray-200 dark:bg-gray-800 py-1 rounded">
      (Solves "Pure Semantics" flaw)
    </div>
  </div>
  <div v-click class="bg-gray-50 dark:bg-[#1a1a1a] p-6 rounded-xl border border-gray-200 dark:border-gray-800 shadow-xl relative mt-4">
    <div class="text-2xl absolute -top-5 left-6 bg-green-500 text-white w-10 h-10 flex items-center justify-center rounded-lg shadow-lg font-bold">2</div>
    <h3 class="text-xl mb-4 mt-2 text-green-500 font-bold border-b border-green-100 dark:border-green-900 pb-2">Semantic Merge Pass</h3>
    <ul class="space-y-3 opacity-90 text-sm">
      <li class="flex items-start gap-2"><carbon-data-structured class="text-green-400 mt-1 flex-shrink-0"/>VLMs extract architectural metadata: <br/><em>Room Type, Facing, Visible Landmarks</em>.</li>
      <li class="flex items-start gap-2"><carbon-arrows-horizontal class="text-blue-400 mt-1 flex-shrink-0"/>Stitches disjoint clusters that share physical space.</li>
    </ul>
    <div class="mt-4 p-2 bg-white dark:bg-black rounded border border-gray-200 dark:border-gray-700 text-xs italic text-center">
      <strong>Example:</strong> Merges "Stage-facing" and "Audience-facing" clusters.
    </div>
  </div>
</div>

---
layout: image-right
image: /images/tree-example.png
backgroundSize: contain
---

# Top-Down Semantic Traversal
<p class="opacity-60 mb-8 font-serif italic">Querying the Scene Efficiently</p>

<div class="mt-4 space-y-4 pr-6">
  <div v-click class="p-6 bg-gradient-to-br from-indigo-600 to-cyan-600 rounded-2xl text-white shadow-xl transform hover:scale-105 transition-transform mb-6">
    <div class="text-xs uppercase tracking-widest opacity-80 mb-2 flex items-center gap-2"><carbon-user/> User Query</div>
    <div class="text-2xl font-serif leading-tight">"Find the fire extinguisher near the exit"</div>
  </div>
  <div v-click class="flex items-center gap-4 p-4 bg-white dark:bg-[#1a1a1a] border border-gray-100 dark:border-gray-800 rounded-xl shadow-md">
    <div class="bg-blue-100 dark:bg-blue-900/40 p-4 rounded-xl"><carbon-function-math class="text-2xl text-blue-600 dark:text-blue-400"/></div>
    <div>
      <h4 class="!m-0 text-lg font-bold">Query Decomposition</h4>
      <p class="!m-0 text-sm opacity-70 mt-1">LLM breaks down the query into logical constraints.</p>
    </div>
  </div>
  <div v-click class="flex items-center gap-4 p-4 bg-white dark:bg-[#1a1a1a] border border-gray-100 dark:border-gray-800 rounded-xl shadow-md">
    <div class="bg-green-100 dark:bg-green-900/40 p-4 rounded-xl"><carbon-tree-view-alt class="text-2xl text-green-600 dark:text-green-400"/></div>
    <div>
      <h4 class="!m-0 text-lg font-bold">Top-Down Traversal</h4>
      <p class="!m-0 text-sm opacity-70 mt-1">Traverses from Root to Leaf using the semantic tree.</p>
    </div>
  </div>
  <div v-click class="flex items-center gap-4 p-4 bg-white dark:bg-[#1a1a1a] border border-gray-100 dark:border-gray-800 rounded-xl shadow-md">
    <div class="bg-purple-100 dark:bg-purple-900/40 p-4 rounded-xl"><carbon-flash class="text-2xl text-purple-600 dark:text-purple-400"/></div>
    <div>
      <h4 class="!m-0 text-lg font-bold">Massive Efficiency</h4>
      <p class="!m-0 text-sm opacity-70 mt-1">Prunes branches using 10-15 word node summaries.</p>
    </div>
  </div>
</div>

---
layout: center
class: text-center
---

# The Localization Problem
<div class="text-xl mt-2 opacity-80 font-serif italic mb-12">VLMs Struggle with Spatial Precision</div>

<div class="max-w-2xl mx-auto">
  <div class="inline-block p-6 rounded-full bg-orange-100 dark:bg-orange-900/20 mb-8">
    <carbon-warning-alt class="text-7xl text-orange-500" />
  </div>
  <p class="text-2xl leading-relaxed font-light">
    We reached the correct leaf views, but... <br/>off-the-shelf VLMs are great at identifying objects, but <strong class="text-orange-500 font-bold">terrible</strong> at drawing precise bounding boxes.
  </p>
  <div v-click class="mt-8 inline-block bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 px-6 py-4 rounded-xl shadow-inner">
    <div class="flex items-center gap-3 text-lg">
      <carbon-ruler-alt class="text-gray-400"/>
      <span>Misaligned by <strong>10-20%</strong> of the image</span>
    </div>
    <div class="text-sm opacity-60 mt-1 uppercase tracking-wider text-center">(Especially for small objects)</div>
  </div>
</div>

---
layout: default
---

# Crop-and-Requery
<p class="opacity-60 mb-12 font-serif italic">Two-Stage Bounding Box Refinement</p>

<div class="grid grid-cols-12 gap-8 relative items-center">
  <div class="col-span-6">
    <div v-click class="mb-6 p-5 bg-white dark:bg-[#1a1a1a] rounded-2xl shadow-lg border-t-4 border-blue-500">
      <div class="flex items-center gap-3 mb-3">
        <div class="bg-blue-500 text-white w-8 h-8 rounded flex items-center justify-center font-bold">1</div>
        <h3 class="text-xl !m-0 font-bold">Spatial CoT</h3>
      </div>
      <p class="opacity-80 text-sm leading-relaxed mb-3">Force VLM to reason about horizontal/vertical thirds and sanity-check spatial relations.</p>
      <div class="px-3 py-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 text-xs rounded-lg font-mono text-center border border-blue-100 dark:border-blue-800">
        <carbon-box class="inline mr-1"/> Yields a *rough* bounding box
      </div>
    </div>
    <div v-click class="p-5 bg-white dark:bg-[#1a1a1a] rounded-2xl shadow-lg border-t-4 border-green-500">
      <div class="flex items-center gap-3 mb-3">
        <div class="bg-green-500 text-white w-8 h-8 rounded flex items-center justify-center font-bold">2</div>
        <h3 class="text-xl !m-0 font-bold">Crop-and-Requery</h3>
      </div>
      <ul class="space-y-3 opacity-80 text-sm">
        <li class="flex items-start gap-2"><carbon-crop class="text-green-500 text-lg mt-0.5 flex-shrink-0"/> Aggressively crop the high-res image around the rough box.</li>
        <li class="flex items-start gap-2"><carbon-chat class="text-blue-500 text-lg mt-0.5 flex-shrink-0"/> Re-prompt the VLM on the zoomed-in crop.</li>
        <li class="flex items-start gap-2"><carbon-map class="text-purple-500 text-lg mt-0.5 flex-shrink-0"/> Map refined coordinates back to original space.</li>
      </ul>
    </div>
  </div>
  <div class="col-span-6">
    <div v-click class="p-2 bg-white dark:bg-gray-800 rounded-xl shadow-xl transform rotate-2 hover:rotate-0 transition-transform">
      <img src="/images/bounding-box.png" class="w-full rounded-lg" alt="Bounding Box Refinement Example" />
    </div>
  </div>
</div>

---
layout: two-cols
---

# Results: Topology
<p class="text-lg opacity-80 mb-8 font-serif">100% Room-Level Topological Accuracy</p>

<div class="pr-8">
  <p class="text-sm opacity-70 mb-6 bg-gray-100 dark:bg-gray-800 p-3 rounded-lg"><carbon-information/> Evaluated on a challenging "Conference Hall" scene with visually diverse but interconnected spaces.</p>
  <div class="space-y-4">
    <div v-click class="p-4 border-l-4 border-red-500 bg-white dark:bg-[#1a1a1a] rounded shadow-sm">
      <div class="font-bold text-red-600 dark:text-red-400 flex items-center gap-2"><carbon-close-outline/> Baseline A (Geometric)</div>
      <div class="text-sm opacity-80 mt-1">Fractured the ballroom (split stage and audience).</div>
    </div>
    <div v-click class="p-4 border-l-4 border-orange-500 bg-white dark:bg-[#1a1a1a] rounded shadow-sm">
      <div class="font-bold text-orange-600 dark:text-orange-400 flex items-center gap-2"><carbon-warning-alt/> Baseline B (Semantic)</div>
      <div class="text-sm opacity-80 mt-1">Hallucinated a merged lobby/corridor due to identical carpets.</div>
    </div>
    <div v-click class="p-4 border-l-4 border-green-500 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded shadow-md transform scale-105 transition-transform mt-6!">
      <div class="font-bold text-green-600 dark:text-green-400 flex items-center gap-2 text-lg"><carbon-checkmark-outline/> Ours (Two-Pass)</div>
      <div class="text-sm opacity-90 mt-2 font-medium">Perfectly isolated distinct rooms while maintaining the integrity of large contiguous spaces.</div>
    </div>
  </div>
</div>

::right::

<div class="pl-4 pt-2">
  <h1 class="!mb-2">Results: Localization</h1>
  <p class="text-lg opacity-80 mb-8 font-serif">34% Improvement in IoU</p>
  <p class="text-sm opacity-70 mb-6 bg-gray-100 dark:bg-gray-800 p-3 rounded-lg"><carbon-information/> Tested on 50 challenging "find" queries for small objects.</p>
  <ul class="space-y-6 mt-8">
    <li v-click class="flex gap-4">
      <div class="bg-red-100 dark:bg-red-900/30 p-3 rounded-full h-fit"><carbon-close-outline class="text-red-500 text-xl"/></div>
      <div>
        <div class="font-bold text-lg">Single-pass VLMs</div>
        <div class="text-sm opacity-80 mt-1">Frequently missed tight boundaries by 10-20%.</div>
      </div>
    </li>
    <li v-click class="flex gap-4">
      <div class="bg-green-100 dark:bg-green-900/30 p-3 rounded-full h-fit"><carbon-checkmark-outline class="text-green-500 text-xl"/></div>
      <div>
        <div class="font-bold text-lg">Crop-and-Requery</div>
        <div class="text-sm opacity-80 mt-1">Tightened bounding boxes strictly to actual pixel boundaries.</div>
      </div>
    </li>
  </ul>
  <div v-click class="mt-12 p-5 bg-gradient-to-br from-indigo-600 to-purple-700 text-white rounded-xl shadow-2xl">
    <h4 class="!m-0 flex items-center gap-2 text-xl font-bold"><carbon-trophy/> Best-View Ranking</h4>
    <p class="!m-0 mt-3 text-sm opacity-90 leading-relaxed">Automatically returns the highest-confidence, most centralized perspective among multiple matches.</p>
  </div>
</div>

---
layout: center
class: text-center
---

# Conclusion & Future Work
<div class="text-xl mt-2 opacity-80 mb-12 font-serif italic">Looking Forward</div>

<div class="max-w-4xl mx-auto space-y-8 text-left">
  <div v-click class="p-8 bg-white dark:bg-[#1a1a1a] rounded-2xl border-l-8 border-blue-500 shadow-xl">
    <h3 class="flex items-center gap-3 text-blue-500 !mt-0 font-bold text-2xl"><carbon-flag/> The Core Takeaway</h3>
    <p class="opacity-80 !mb-0 text-lg leading-relaxed mt-4">Off-the-shelf 2D VLMs can drive precise 3D scene reasoning <strong class="text-blue-500 dark:text-blue-400">without</strong> complex 3D feature distillation, provided we use robust clustering and refinement pipelines.</p>
  </div>
  <div class="grid grid-cols-2 gap-8">
    <div v-click class="p-6 bg-white dark:bg-[#1a1a1a] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-lg">
      <div class="bg-purple-100 dark:bg-purple-900/30 w-12 h-12 rounded-xl flex items-center justify-center mb-4">
        <carbon-3d-curve-auto-colon class="text-purple-600 dark:text-purple-400 text-2xl"/>
      </div>
      <div class="font-bold text-lg mb-2">3D Depth Unprojection</div>
      <p class="opacity-70 !mb-0 text-sm leading-relaxed">Transitioning from refined 2D bounding boxes to exact 3D world coordinates using 3DGS depth maps.</p>
    </div>
    <div v-click class="p-6 bg-white dark:bg-[#1a1a1a] rounded-2xl border border-gray-200 dark:border-gray-800 shadow-lg">
      <div class="bg-green-100 dark:bg-green-900/30 w-12 h-12 rounded-xl flex items-center justify-center mb-4">
        <carbon-camera-action class="text-green-600 dark:text-green-400 text-2xl"/>
      </div>
      <div class="font-bold text-lg mb-2">Automated Capture</div>
      <p class="opacity-70 !mb-0 text-sm leading-relaxed">Integrating automated camera placement algorithms (e.g., NoField) to eliminate manual scene capture.</p>
    </div>
  </div>
</div>

---
layout: center
class: text-center
---

<div class="flex justify-center mb-8">
  <div class="w-32 h-32 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-full flex items-center justify-center shadow-2xl animate-bounce-slow">
    <carbon-cube class="text-6xl text-white"/>
  </div>
</div>

<h1 class="text-6xl font-bold font-serif bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-cyan-500 dark:from-blue-400 dark:to-cyan-300">
  Thank You!
</h1>

<p class="mt-6 text-xl opacity-70">
  Any Questions?
</p>

<div class="mt-16 text-sm opacity-50 flex justify-center gap-6">
  <span class="flex items-center gap-1"><carbon-logo-github/> SemanticSplat</span>
</div>
