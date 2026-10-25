# 📋 Google Form Submission Kit & Quick Copy-Paste Template
### Aligned with TIET UCS503 "The Cycle" Standards

Use this document to quickly fill out and submit all deliverables to your Google Form. Everything is formatted and ready to copy-paste.

---

## 🎯 1. Direct Field Answers (Copy & Paste)

### **Candidate / Student Name**:
```text
Robin
```

### **Project / Submission Title**:
```text
Dijkstra's Shortest Path Algorithm: Grounded SOT RAG System, Dual-Language Video Suite & Interactive Assessment Platform
```

### **Chosen DSA Topic**:
```text
Dijkstra's Algorithm (Single-Source Shortest Paths in Weighted Graphs)
```

### **Single Source of Truth (SOT) Used**:
```text
1. GeeksforGeeks (GFG): Core SSSP Guide (Adjacency Matrix O(V²)), Min-Heap Guide (O((V + E) log V)), C++ std::set Guide, Negative Weights Breakdown, and Real-World Applications (OSPF, GPS).
2. MIT OpenCourseWare 6.006 (Fall 2011, Lecture 16: Dijkstra): Taught by Prof. Erik Demaine & Prof. Srinivas Devadas (Edge relaxation invariant proofs, triangle inequality, upper-bound property).
```

### **Languages Supported for Voice-Over & Narration**:
```text
Dual-Language Support with Interactive User Selector:
1. English: Neural Voice (en-US-ChristopherNeural) with synchronized 1080p MP4 animated walkthrough.
2. Hindi (हिंदी): Neural Voice (hi-IN-MadhurNeural) with synchronized 1080p MP4 animated walkthrough.
Both options feature complete synchronized bilingual subtitles (English & Hindi).
```

### **Multi-Modal Interactive Features Included**:
```text
1. Grounded RAG Chatbot with Citation & Verification Safeguards
2. Native Dual-Language 1080p Video Walkthrough Player (English & Hindi)
3. Animated Interactive Visuals Gallery ("Interactive Photos") for Relaxation, Negative Edges, and Complexities
4. 17-Step Interactive SVG Graph Simulator with Priority Queue Inspector
5. Interactive Dijkstra Knowledge Quiz with Automated Evaluation & Grounded Explanations
6. 9-Slide PowerPoint Presentation (.pptx) & Interactive HTML5 Slide Deck
7. Comprehensive Study Material Archive with Official MIT PDF & JSON Manifest
```

---

## 🔄 2. Alignment with "The Cycle" (TIET UCS503 Conduct & Engineering Framework)
*Reference: https://tiet-ucs503.github.io/bug-bounty/conduct/the-cycle/index.html*

| Step of The Cycle | Implementation in this Project |
| :--- | :--- |
| **1. Concept (What, For Whom)** | A single-source-of-truth grounded RAG platform providing mathematically rigorous answers on Dijkstra's algorithm, with multi-modal dual-language video/audio walkthroughs and interactive assessment. |
| **2. Contract (What Others May Rely On)** | Strict RAG response contract (`{query, answer, confidence_score, citations, exact_quotes}`), deterministic graph simulation states (17 steps), standard H.264 MP4 videos, and synchronized bilingual subtitle cues. |
| **3. Tests (How We Measure It)** | Automated test suite `test_rag.py` executing 5 semantic query checks, edge relaxation verification, out-of-scope rejection test, quiz engine validation, and disk deliverable verifications. |
| **4. Implementation (The Code)** | Pure-Python hybrid search (BM25 + TF-IDF cosine similarity), edge-tts neural synthesis, matplotlib + imageio-ffmpeg video generation, and native Gradio UI. |
| **5. Refinement (Run, Read, Change)** | Replaced fragile 1MB base64 iframe embedding with native `gr.Video` and `gr.Audio` streaming (resolving display issues), added dual-language switcher, built interactive visual proofs, and incorporated interactive quiz. |

---

## 🔗 3. Files & Links to Submit in the Form

| Form Field | What to Provide | Local File Path |
| :--- | :--- | :--- |
| **Complete Deliverables ZIP** | Upload `Dijkstra_RAG_Deliverables_Robin.zip` to Google Drive & paste share link | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\Dijkstra_RAG_Deliverables_Robin.zip` |
| **English Walkthrough Video (MP4)** | Upload `dijkstra_walkthrough_english.mp4` to Drive / Form | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\dijkstra_walkthrough_english.mp4` |
| **Hindi Walkthrough Video (MP4)** | Upload `dijkstra_walkthrough_hindi.mp4` to Drive / Form | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\dijkstra_walkthrough_hindi.mp4` |
| **Presentation Slide Deck (.pptx)** | Upload `Dijkstra_Algorithm_Complete_Guide.pptx` | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\Dijkstra_Algorithm_Complete_Guide.pptx` |
| **Official MIT Lecture 16 PDF** | Upload `MIT6_006F11_lec16.pdf` (809 KB) | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\data\archive\MIT6_006F11_lec16.pdf` |
| **Sources Manifest (JSON)** | Upload `sources_manifest.json` | `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\data\archive\sources_manifest.json` |
| **Live App URL (Hugging Face)** | `https://huggingface.co/spaces/<your-username>/dijkstra-sssp-rag` | Deployed via `deploy_hf.py` |

---

## 📝 4. Comprehensive Abstract / Description (Ready to Paste)

```text
Project Overview:
I have engineered a production-grade, custom-built Retrieval-Augmented Generation (RAG) system and multi-modal learning suite grounded in a single source of truth: lecture and tutorial content on Dijkstra's Shortest Path Algorithm from GeeksforGeeks (GFG) and MIT 6.006 (Prof. Erik Demaine & Prof. Srinivas Devadas).

The engineering process strictly adhered to "The Cycle" (Concept -> Contract -> Tests -> Implementation -> Refinement):

1. Strict Single-Source-of-Truth Grounding:
   - The hybrid retrieval engine indexes 55 semantic chunks across authentic GFG guides and MIT Lecture 16.
   - Out-of-scope topics (e.g., QuickSort, dynamic programming) are cleanly rejected with 0% false confidence.
   - Clean mathematical formatting without raw LaTeX dollar signs (O(V²), O((V + E) log V), δ(s, v), w(u, v) ≥ 0).

2. Dual-Language Video & Voice-Over Suite:
   - Supports both English (en-US-ChristopherNeural) and Hindi (hi-IN-MadhurNeural) neural narrations.
   - High-definition 1080p MP4 videos rendered with synchronized graph animations, node lighting, and edge relaxation.
   - Complete bilingual subtitles (English & Hindi) synchronized across all narration cues.

3. Animated Interactive Visuals Gallery ("Interactive Photos"):
   - Visual 1: Edge Relaxation Mechanism (d[u] + w(u, v) < d[v] upper-bound tightening).
   - Visual 2: The 3-Node Negative Edge Counterexample (proving why greedy choice fails).
   - Visual 3: Adjacency Matrix O(V²) vs Min-Heap O((V + E) log V) architecture comparison.
   - Visual 4: Shortest Path Tree (SPT) Invariant & Frontier Partition (MIT 6.006 Cut Property).

4. Interactive Step-by-Step Graph Simulator:
   - 17-step deterministic Dijkstra execution on a 6-node weighted graph.
   - Live SVG rendering with dynamic Priority Queue inspection and tentative distance table.

5. Interactive Assessment Quiz:
   - 6 multiple-choice questions testing algorithmic invariants, complexity trade-offs, and applications.
   - Instant scoring, mastery badges, and grounded rationales quoting GFG and MIT 6.006.

6. Presentation Slides:
   - Downloadable 9-slide PowerPoint deck (.pptx) and embedded interactive HTML5 presentation.
```

---

## ☁️ 5. Quick Google Drive & Hugging Face Upload Steps

### If the Google Form asks for Google Drive Links:
1. Open [Google Drive](https://drive.google.com).
2. Click **New > File upload** and upload:
   - `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\Dijkstra_RAG_Deliverables_Robin.zip`
   - `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\dijkstra_walkthrough_english.mp4`
   - `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\dijkstra_walkthrough_hindi.mp4`
   - `C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission\static\Dijkstra_Algorithm_Complete_Guide.pptx`
3. Right-click each uploaded file, click **Share > Change to "Anyone with the link can view"**, click **Copy link**, and paste it into the Google Form.

### If deploying to Hugging Face Spaces:
1. In terminal:
   ```powershell
   cd C:\Users\robin\OneDrive\Desktop\Dijkstra_RAG_Submission
   .venv\Scripts\python deploy_hf.py --repo <your-username>/dijkstra-sssp-rag --token <your-hf-token>
   ```
2. Paste the live space URL into the Google Form.
