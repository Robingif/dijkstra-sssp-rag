---
title: Dijkstra Shortest Path Grounded RAG Platform
emoji: 🛣️
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
license: apache-2.0
short_description: Grounded RAG Platform for Dijkstra's Algorithm
---

# 🛣️ Dijkstra's Shortest Path Algorithm: Grounded RAG & Learning Platform

A comprehensive, production-grade Retrieval-Augmented Generation (RAG) system and interactive learning platform answering questions strictly grounded in a single source of truth: **GeeksforGeeks (GFG)** and **MIT 6.006 Lecture 16 (Prof. Erik Demaine & Prof. Srinivas Devadas)**.

Built **100% from scratch** by **Robin**, featuring an AI-augmented RAG engine, an interactive step-by-step graph visualizer, a slide deck (`.pptx` + HTML5), and a multimedia video animation with **local language (Hindi) neural voice-over**.

---

## 🌟 Key Features

1. **💬 Strict Grounded RAG Assistant**:
   - Zero-hallucination guardrail: Answers are strictly grounded in indexed study materials.
   - Out-of-domain detection: Automatically rejects queries unrelated to Dijkstra's algorithm.
   - Mathematical derivations with LaTeX formatting ($O((V+E)\log V)$, $\text{Relax}(u, v, w)$).
   - Verifiable source citations with relevance scores, page markers, and URLs.

2. **📚 Transparent Study Materials Archive**:
   - Built-in reader for all GeeksforGeeks reference guides (Adjacency Matrix, Min-Heap, `std::set`, Negative Weights, Applications).
   - Full 828 KB official MIT 6.006 Lecture 16 PDF (`MIT6_006F11_lec16.pdf`) by Prof. Demaine & Devadas available for viewing and direct download.
   - Transparent JSON sources manifest (`sources_manifest.json`) listing every single external reference.

3. **⚡ Step-by-Step Interactive Graph Simulator**:
   - Live SVG canvas showing Dijkstra's algorithm executing on a 6-node weighted graph.
   - Real-time Shortest Path Tree (SPT) edge locking and glowing node states.
   - Live Priority Queue inspector and Tentative Distance Table ($d[v]$) at every relaxation step.

4. **📊 Master Slide Deck Presentation**:
   - Downloadable PowerPoint presentation (`Dijkstra_Algorithm_Complete_Guide.pptx`) with 9 beautifully styled slides.
   - Embedded interactive HTML5 presentation with keyboard arrow navigation.

5. **🎬 Video Animation & Hindi Voice-Over**:
   - Step-by-step video animation synchronized with graph state updates.
   - High-fidelity **Hindi neural voice-over** (`hi-IN-MadhurNeural`) generated via `edge-tts`.
   - Dual-language subtitle system (Hindi and English).

---

## 📁 Repository Structure

```text
dijkstra-rag/
├── app.py                      # Main Gradio application (Hugging Face Spaces entry point)
├── rag_engine.py               # Custom hybrid retrieval & grounding engine
├── graph_simulator.py          # Interactive Dijkstra graph simulation & SVG renderer
├── slides_generator.py         # Generates PPTX and HTML5 slide decks
├── media_generator.py          # Generates Hindi neural voiceover & synchronized video player
├── requirements.txt            # Python dependencies
├── README.md                   # Space configuration & project documentation
├── data/
│   └── archive/
│       ├── sources_manifest.json            # Transparent sources catalog
│       ├── gfg_dijkstra_matrix.md           # GFG Adjacency Matrix guide O(V²)
│       ├── gfg_dijkstra_minheap.md          # GFG Min-Heap guide O((V+E)log V)
│       ├── gfg_dijkstra_set.md              # GFG std::set guide
│       ├── gfg_dijkstra_negative_weights.md # GFG Negative weight breakdown
│       ├── gfg_dijkstra_applications.md     # GFG Applications (OSPF, GPS)
│       ├── mit_6006_lec16_dijkstra.md       # MIT 6.006 Lecture 16 notes & proofs
│       └── MIT6_006F11_lec16.pdf            # Official MIT Lecture 16 PDF (828 KB)
└── static/
    ├── Dijkstra_Algorithm_Complete_Guide.pptx # Downloadable slide deck
    ├── slides.html                           # Interactive HTML5 presentation
    ├── dijkstra_voiceover_hindi.mp3          # Synthesized Hindi voice-over
    └── video_player.html                     # Synchronized animation player
```

---

## 🚀 How to Run Locally

```bash
# 1. Clone repository
git clone https://huggingface.co/spaces/robinsingla/dijkstra-sssp-rag
cd dijkstra-sssp-rag

# 2. Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch web application
python app.py
```
Open `http://127.0.0.1:7860` in your web browser.

---

## ☁️ How to Deploy to Hugging Face Spaces

1. Create a new Space on [Hugging Face](https://huggingface.co/new-space):
   - **Space Name**: `dijkstra-sssp-rag`
   - **SDK**: `Gradio`
   - **License**: `Apache-2.0`
2. Push this repository to your Space:
   ```bash
   git init
   git remote add space https://huggingface.co/spaces/robinsingla/dijkstra-sssp-rag
   git add .
   git commit -m "Deploy Dijkstra Grounded RAG Platform"
   git push space main
   ```
3. Your Space will build and launch automatically!

---

## 📜 Citations & Sources of Truth

All materials used in this project are publicly available educational resources:
1. **GeeksforGeeks**: [Dijkstra's Shortest Path Algorithm (Greedy Algo-7)](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)
2. **GeeksforGeeks**: [Dijkstra's Algorithm for Adjacency List (Greedy Algo-8)](https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/)
3. **GeeksforGeeks**: [Dijkstra's Shortest Path Algorithm using Set in STL](https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-set-in-stl/)
4. **GeeksforGeeks**: [Why Does Dijkstra's Algorithm Fail on Negative Weights?](https://www.geeksforgeeks.org/why-does-dijkstras-algorithm-fail-on-negative-weights/)
5. **GeeksforGeeks**: [Applications of Dijkstra's Shortest Path Algorithm](https://www.geeksforgeeks.org/applications-of-dijkstras-shortest-path-algorithm/)
6. **MIT OpenCourseWare**: [MIT 6.006 Introduction to Algorithms, Fall 2011 - Lecture 16: Dijkstra](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/mit6_006f11_lec16/), taught by Prof. Erik Demaine & Prof. Srinivas Devadas.

---
*Created by Robin • Grounded Algorithm Engineering System*
