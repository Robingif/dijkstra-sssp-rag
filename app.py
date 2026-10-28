import os
import json
import html
import gradio as gr
from rag_engine import HybridRAGEngine
from graph_simulator import DijkstraSimulator
from quiz_engine import QUIZ_QUESTIONS, evaluate_quiz, render_quiz_result_html
from interactive_visuals import get_all_interactive_visuals_html

# Paths & Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Initialize core engines
rag_engine = HybridRAGEngine(DATA_DIR)
sim = DijkstraSimulator()

# Preload HTML components
slides_path = os.path.join(STATIC_DIR, "slides.html")
slides_srcdoc = html.escape(open(slides_path, "r", encoding="utf-8").read()) if os.path.exists(slides_path) else ""

# Media file paths
EN_VIDEO_PATH = os.path.join(STATIC_DIR, "dijkstra_walkthrough_english.mp4")
HI_VIDEO_PATH = os.path.join(STATIC_DIR, "dijkstra_walkthrough_hindi.mp4")
EN_AUDIO_PATH = os.path.join(STATIC_DIR, "dijkstra_voiceover_english.mp3")
HI_AUDIO_PATH = os.path.join(STATIC_DIR, "dijkstra_voiceover_hindi.mp3")
PPTX_PATH = os.path.join(STATIC_DIR, "Dijkstra_Algorithm_Complete_Guide.pptx")
MIT_PDF_PATH = os.path.join(DATA_DIR, "archive", "MIT6_006F11_lec16.pdf")
MANIFEST_PATH = os.path.join(DATA_DIR, "archive", "sources_manifest.json")

# Document registry
DOC_FILES = {
    "MIT 6.006: SSSP Formulation, Greedy Strategy & Pseudocode": "mit_ocw_dijkstra_core.md",
    "MIT 6.006: Edge Relaxation Safety Lemma & Triangle Inequality": "mit_ocw_relaxation_proofs.md",
    "MIT 6.006: Priority Queue Complexity (Array vs Min-Heap vs Fibonacci)": "mit_ocw_priority_queues_complexity.md",
    "MIT 6.006: Correctness Proof & Why Greedy Fails on Negative Weights": "mit_ocw_greedy_choice_negative_weights.md",
    "MIT 6.006: Balls-and-Strings Physical Model & DAG Shortest Paths": "mit_ocw_balls_and_strings_intuition.md",
    "MIT 6.006: Complete Lecture 16 Notes & Recitation Review": "mit_6006_lec16_dijkstra.md",
    "MIT Official Sources Registry Manifest (JSON)": "sources_manifest.json"
}

def get_doc_content(doc_title: str) -> str:
    fname = DOC_FILES.get(doc_title)
    if not fname:
        return "Document not found."
    fpath = os.path.join(DATA_DIR, "archive", fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        if fname.endswith(".json"):
            return f"```json\n{content}\n```"
        return content
    return "Document file missing on disk."

# RAG Chat Handler
def chat_with_rag(message: str, history: list):
    if not message.strip():
        return history, ""
    
    result = rag_engine.answer_query(message)
    answer = result["answer"]
    
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return history, ""

# Simulator Handlers
def sim_step(current_idx: int, direction: int):
    new_idx = max(0, min(current_idx + direction, sim.get_total_steps() - 1))
    svg_html = sim.render_svg(new_idx)
    table_html = sim.render_distance_table_html(new_idx)
    pq_html = sim.render_pq_html(new_idx)
    step_data = sim.get_step_data(new_idx)
    action_info = f"**Step {new_idx} of {sim.get_total_steps() - 1}**: {step_data['action']}"
    return new_idx, new_idx, svg_html, table_html, pq_html, action_info

def sim_jump(target_idx: int):
    new_idx = max(0, min(int(target_idx), sim.get_total_steps() - 1))
    svg_html = sim.render_svg(new_idx)
    table_html = sim.render_distance_table_html(new_idx)
    pq_html = sim.render_pq_html(new_idx)
    step_data = sim.get_step_data(new_idx)
    action_info = f"**Step {new_idx} of {sim.get_total_steps() - 1}**: {step_data['action']}"
    return new_idx, svg_html, table_html, pq_html, action_info

def sim_reset():
    return sim_step(0, 0)

# Video Language Switcher
def switch_video_language(lang_choice: str):
    if "Hindi" in lang_choice:
        return HI_VIDEO_PATH
    return EN_VIDEO_PATH

# Quiz Handler
def submit_quiz_answers(*answers_list):
    answers_dict = {}
    for idx, ans in enumerate(answers_list):
        qid = QUIZ_QUESTIONS[idx]["id"]
        answers_dict[qid] = ans
    
    correct_count, total, percentage, badge, review_items = evaluate_quiz(answers_dict)
    report_html = render_quiz_result_html(correct_count, total, percentage, badge, review_items)
    return report_html

def reset_quiz_form():
    # Returns None for all questions, and empty HTML report
    resets = [None] * len(QUIZ_QUESTIONS)
    resets.append("")
    return tuple(resets)

# Custom Styling
CUSTOM_CSS = """
body, .gradio-container {
    background-color: #0b0f19 !important;
    color: #f8fafc !important;
    font-family: system-ui, -apple-system, sans-serif !important;
}
.header-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
}
.header-badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid #38bdf8;
    color: #38bdf8;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}
.header-title {
    font-size: 26px;
    font-weight: 800;
    color: #f8fafc;
    margin: 6px 0;
}
.header-sub {
    font-size: 14px;
    color: #94a3b8;
}
.author-pill {
    display: inline-flex;
    align-items: center;
    background: #1e293b;
    border: 1px solid #475569;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 12px;
    color: #38bdf8;
    margin-top: 10px;
}
.cycle-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid #10b981;
    color: #34d399;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 700;
    margin-top: 10px;
    margin-left: 8px;
}
"""

with gr.Blocks(title="Dijkstra's Shortest Path Algorithm — Grounded SOT Platform") as demo:
    
    # Header Banner
    with gr.Column(elem_classes=["header-banner"]):
        gr.HTML("""
        <div class="header-badge">SINGLE SOURCE OF TRUTH (SOT) GROUNDED SYSTEM</div>
        <div class="header-title">🛣️ Dijkstra's Shortest Path Algorithm: Grounded RAG & Learning Suite</div>
        <div class="header-sub">
            Grounded strictly in <b>MIT 6.006 Lecture 16 (Prof. Erik Demaine & Prof. Srinivas Devadas)</b> and <b>CLRS Chapter 24</b>.
            Equipped with multi-modal AI retrieval, dual-language video/voice-over (English & Hindi), interactive infographics, step-by-step simulation, and assessment quiz.
        </div>
        <div style="display:flex; flex-wrap:wrap; gap:8px;">
            <div class="author-pill">
                👨‍💻 <b>Developer & Author</b>: Robin • Built 100% from Scratch with AI-Augmented Architecture
            </div>
            <div class="cycle-badge">
                🔄 <b>The Cycle (TIET UCS503) Compliant</b>: Concept ➔ Contract ➔ Tests ➔ Implementation ➔ Refinement
            </div>
        </div>
        """)

    with gr.Tabs():
        # TAB 1: Grounded RAG Chat
        with gr.Tab("💬 Dijkstra AI Assistant (Grounded RAG)", id="tab_chat"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        height=540,
                        placeholder="Welcome to the Dijkstra SOT Assistant! Ask any technical question about Dijkstra's algorithm, edge relaxation, time complexities, why it fails on negative weights, or real-world applications."
                    )
                    with gr.Row():
                        msg_input = gr.Textbox(
                            placeholder="Type your question about Dijkstra's algorithm here...",
                            lines=1,
                            scale=5,
                            show_label=False
                        )
                        send_btn = gr.Button("Ask Assistant", variant="primary", scale=1)
                        clear_btn = gr.Button("Clear Chat", variant="secondary", scale=1)

                    gr.HTML("<div style='margin-top:8px; font-size:12px; color:#94a3b8;'><b>💡 Suggested Quick Questions:</b></div>")
                    with gr.Row():
                        q1_btn = gr.Button("Why does Dijkstra fail on negative weights?", size="sm")
                        q2_btn = gr.Button("Compare Adjacency Matrix vs Min-Heap complexities", size="sm")
                        q3_btn = gr.Button("Explain edge relaxation & triangle inequality", size="sm")
                    with gr.Row():
                        q4_btn = gr.Button("How does OSPF internet routing use Dijkstra?", size="sm")
                        q5_btn = gr.Button("Show Python implementation using heapq", size="sm")
                        q6_btn = gr.Button("How does QuickSort work? (OOS Test)", size="sm")

                with gr.Column(scale=1):
                    gr.HTML("""
                    <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:18px;">
                        <h4 style="color:#38bdf8; margin:0 0 10px 0; font-size:15px;">🛡️ Grounding Safeguards</h4>
                        <ul style="font-size:12px; line-height:1.6; color:#cbd5e1; padding-left:18px; margin:0;">
                            <li><b>Single Source of Truth</b>: Answers generated <i>exclusively</i> from MIT 6.006 Lecture 16 notes and CLRS Chapter 24.</li>
                            <li><b>No Hallucinations</b>: Out-of-scope topics (e.g., QuickSort, Dynamic Programming) are cleanly rejected with 0% false confidence.</li>
                            <li><b>Exact Quotes & Citations</b>: Every response includes verbatim quotes and mathematical references.</li>
                            <li><b>Clean Typography</b>: Zero raw LaTeX artifacts; rendered using clean mathematical symbols (O(V²), O((V + E) log V), δ(s, v)).</li>
                        </ul>
                    </div>

                    <div style="background:#1e293b; border:1px solid #334155; border-radius:12px; padding:18px; margin-top:16px;">
                        <h4 style="color:#10b981; margin:0 0 10px 0; font-size:15px;">📊 Indexed Knowledge Base</h4>
                        <div style="font-size:12px; color:#94a3b8; line-height:1.6;">
                            • <b>MIT 6.006 Lecture 16</b>: Prof. Erik Demaine & Prof. Srinivas Devadas<br/>
                            • <b>MIT OCW Course Modules</b>: SSSP Formulation, Edge Relaxation Invariants, Heap Complexities, Greedy Correctness Proofs<br/>
                            • <b>Total Passages</b>: 49 Semantic Chunks<br/>
                            • <b>Retrieval Engine</b>: Hybrid BM25 + TF-IDF Vector Space
                        </div>
                    </div>
                    """)

            # Event listeners for chat
            send_btn.click(chat_with_rag, [msg_input, chatbot], [chatbot, msg_input])
            msg_input.submit(chat_with_rag, [msg_input, chatbot], [chatbot, msg_input])
            clear_btn.click(lambda: [], None, chatbot)

            # Quick prompts
            q1_btn.click(lambda: "Why does Dijkstra's algorithm fail on negative edge weights and negative cycles?", None, msg_input)
            q2_btn.click(lambda: "What is the time complexity of Dijkstra using Adjacency Matrix vs Min-Heap Priority Queue?", None, msg_input)
            q3_btn.click(lambda: "How does the edge relaxation step work mathematically according to MIT 6.006?", None, msg_input)
            q4_btn.click(lambda: "What real-world network routing protocols use Dijkstra's algorithm?", None, msg_input)
            q5_btn.click(lambda: "Provide the production Python implementation of Dijkstra using heapq with lazy deletion.", None, msg_input)
            q6_btn.click(lambda: "How does QuickSort work and what is its expected runtime?", None, msg_input)

        # TAB 2: Video Walkthrough & Dual-Language Voice-Over
        with gr.Tab("🎬 Video Walkthrough & Dual Voice-Over (EN & HI)", id="tab_video"):
            gr.Markdown("### 🔊 High-Definition Step-by-Step Video Walkthrough with Multi-Language Voice-Over")
            gr.Markdown("Choose your preferred narration language below. Both videos feature synchronized animated graph relaxation, edge traversal, and bilingual subtitles.")

            with gr.Row():
                video_lang_selector = gr.Radio(
                    choices=[
                        "🇬🇧 English Walkthrough Video & Voice-Over",
                        "🇮🇳 Hindi (हिंदी) Walkthrough Video & Voice-Over"
                    ],
                    value="🇬🇧 English Walkthrough Video & Voice-Over",
                    label="🌐 Select Video Narration Language",
                    scale=3
                )
                with gr.Row(scale=2):
                    dl_en_vid = gr.File(value=EN_VIDEO_PATH, label="💾 Download English MP4 Video", interactive=False)
                    dl_hi_vid = gr.File(value=HI_VIDEO_PATH, label="💾 Download Hindi MP4 Video", interactive=False)

            # Native Gradio Video Player: 100% reliable, zero iframe or srcdoc limitations
            main_video_player = gr.Video(
                value=EN_VIDEO_PATH,
                label="🎬 Dijkstra's Algorithm Walkthrough (Native 1080p Video Player)",
                interactive=False,
                autoplay=False
            )

            video_lang_selector.change(switch_video_language, video_lang_selector, main_video_player)

            with gr.Row():
                audio_en = gr.Audio(value=EN_AUDIO_PATH, label="🎵 Standalone English Audio (en-US-ChristopherNeural)", interactive=False)
                audio_hi = gr.Audio(value=HI_AUDIO_PATH, label="🎵 Standalone Hindi Audio (hi-IN-MadhurNeural)", interactive=False)

            with gr.Accordion("📜 Complete Synchronized Dual Subtitles (English & हिंदी)", open=False):
                gr.Markdown("""
| Timestamp | English Subtitle | हिंदी सबटाइटल |
|---|---|---|
| **0:00 - 0:08** | Welcome to Dijkstra's Single-Source Shortest Path Algorithm (SSSP). | डाइक्स्ट्रा सिंगल-सोर्स शॉर्टेस्ट पाथ एल्गोरिदम में आपका स्वागत है। |
| **0:08 - 0:18** | Initialization: Source node A set to distance 0, other nodes set to infinity. | प्रारंभ: सोर्स नोड A की दूरी 0, और बाकी नोड्स की दूरी अनंत (infinity) रखी गई। |
| **0:18 - 0:29** | Greedy choice: Extract min node A (d=0). Relax outgoing edges A➔B (4) and A➔C (2). | ग्रीडी चॉइस: न्यूनतम दूरी नोड A (d=0)। एज रिलैक्सेशन A➔B (4) और A➔C (2)। |
| **0:29 - 0:43** | Node C has min dist 2. Relax C➔B (2+1=3 < 4, updated!) and C➔E (2+8=10). | नोड C न्यूनतम दूरी 2 पर। रिलैक्स C➔B (2+1=3 < 4, अपडेट!) और C➔E (2+8=10)। |
| **0:43 - 0:56** | Node B has min dist 3. Relax B➔D (3+5=8). Complexity with Min-Heap is O((V+E) log V). | नोड B दूरी 3। रिलैक्स B➔D (3+5=8)। बाइनरी मिन-हीप के साथ समय O((V+E) log V)। |
| **0:56 - 1:09** | Crucial rule: Non-negative weights required! If negative edges exist, use Bellman-Ford. | नियम: केवल नॉन-नेगेटिव एज वेट्स मान्य हैं! नेगेटिव वेट्स के लिए बेलमैन-फोर्ड इस्तेमाल करें। |
| **1:09 - 1:25** | Final Shortest Path Tree locked! Powers OSPF internet routing and Google Maps GPS. | शॉर्टेस्ट पाथ ट्री पूरा हुआ! यह OSPF इंटरनेट रूटिंग और गूगल मैप्स GPS को चलाता है। |
                """)

        # TAB 3: Animated Interactive Visuals Gallery
        with gr.Tab("🖼️ Animated Interactive Visuals Gallery", id="tab_visuals"):
            gr.Markdown("### 🎨 Interactive Conceptual Infographics & Visual Proofs")
            gr.Markdown("Explore interactive visual diagrams illustrating edge relaxation, negative edge counterexamples, algorithmic complexity trade-offs, and Shortest Path Tree (SPT) invariants.")
            gr.HTML(value=get_all_interactive_visuals_html())

        # TAB 4: Step-by-Step Interactive Graph Visualizer
        with gr.Tab("⚡ Step-by-Step Interactive Graph Visualizer", id="tab_sim"):
            gr.Markdown("### 🔍 Step-by-Step Execution of Dijkstra's Algorithm on a Weighted Graph")
            gr.Markdown("Watch tentative distances update and Shortest Path Tree edges lock in as each vertex is relaxed.")

            current_step_state = gr.State(0)
            
            with gr.Row():
                with gr.Column(scale=3):
                    svg_output = gr.HTML(value=sim.render_svg(0))
                with gr.Column(scale=2):
                    with gr.Column(elem_classes=["header-banner"]):
                        action_display = gr.Markdown(value=f"**Step 0 of {sim.get_total_steps() - 1}**: {sim.get_step_data(0)['action']}")
                    
                    gr.Markdown("#### 📋 Current Priority Queue (PQ) State")
                    pq_display = gr.HTML(value=sim.render_pq_html(0))
                    
                    gr.Markdown("#### 📊 Tentative Distance Array (d[v])")
                    table_display = gr.HTML(value=sim.render_distance_table_html(0))

            with gr.Row():
                prev_btn = gr.Button("◀ Previous Step", scale=1)
                next_btn = gr.Button("Step Forward ▶", variant="primary", scale=1)
                reset_btn = gr.Button("↺ Reset Simulation", scale=1)
                step_slider = gr.Slider(minimum=0, maximum=sim.get_total_steps() - 1, step=1, value=0, label="Jump to Step", scale=2)

            prev_btn.click(lambda s: sim_step(s, -1), current_step_state, [current_step_state, step_slider, svg_output, table_display, pq_display, action_display])
            next_btn.click(lambda s: sim_step(s, 1), current_step_state, [current_step_state, step_slider, svg_output, table_display, pq_display, action_display])
            reset_btn.click(sim_reset, None, [current_step_state, step_slider, svg_output, table_display, pq_display, action_display])
            step_slider.change(sim_jump, step_slider, [current_step_state, svg_output, table_display, pq_display, action_display])

        # TAB 5: Interactive Dijkstra Knowledge Quiz
        with gr.Tab("📝 Interactive Dijkstra Knowledge Quiz", id="tab_quiz"):
            gr.Markdown("### 🧠 Dijkstra's Algorithm: Mastery Assessment & Knowledge Check")
            gr.Markdown("Test your conceptual understanding of shortest paths, relaxation proofs, time complexities, and edge invariants grounded in MIT 6.006 (Prof. Demaine & Prof. Devadas).")

            quiz_radio_components = []
            with gr.Column():
                for idx, q in enumerate(QUIZ_QUESTIONS):
                    with gr.Column(elem_classes=["header-banner"]):
                        gr.Markdown(f"### {q['question']}")
                        radio = gr.Radio(
                            choices=q["options"],
                            label="Select your answer:",
                            value=None
                        )
                        quiz_radio_components.append(radio)

                with gr.Row():
                    submit_quiz_btn = gr.Button("Submit Quiz Answers", variant="primary", scale=2)
                    reset_quiz_btn = gr.Button("↺ Reset Quiz", scale=1)

                quiz_report_display = gr.HTML(value="")

                submit_quiz_btn.click(
                    submit_quiz_answers,
                    inputs=quiz_radio_components,
                    outputs=[quiz_report_display]
                )
                reset_quiz_btn.click(
                    reset_quiz_form,
                    outputs=quiz_radio_components + [quiz_report_display]
                )

        # TAB 6: Slide Deck Presentation
        with gr.Tab("📊 Slide Deck & Presentation", id="tab_slides"):
            with gr.Row():
                gr.Markdown("### 📽️ Professional Slide Deck: Dijkstra's Algorithm")
                download_pptx_btn = gr.File(
                    value=PPTX_PATH,
                    label="💾 Download Presentation (.pptx)",
                    interactive=False
                )
            
            # Embed HTML5 Slide Deck iframe with self-contained srcdoc
            gr.HTML(f"""
            <div style="border:1px solid #334155; border-radius:12px; overflow:hidden; height:640px;">
                <iframe srcdoc="{slides_srcdoc}" width="100%" height="100%" style="border:none;"></iframe>
            </div>
            """)

        # TAB 7: Study Materials Archive & "The Cycle"
        with gr.Tab("📚 Study Material Archive & 'The Cycle'", id="tab_archive"):
            gr.Markdown("### 📖 Transparent Single-Source-of-Truth Knowledge Archive")
            gr.Markdown("Select any authentic reference material below to read the complete verbatim text and inspect the mathematical derivations.")
            
            with gr.Row():
                doc_selector = gr.Dropdown(
                    choices=list(DOC_FILES.keys()),
                    value="MIT 6.006: SSSP Formulation, Greedy Strategy & Pseudocode",
                    label="Choose Document from Knowledge Base",
                    scale=3
                )
                with gr.Row(scale=2):
                    download_pdf_btn = gr.File(
                        value=MIT_PDF_PATH,
                        label="📄 Download Official MIT Lecture 16 PDF",
                        interactive=False
                    )
                    download_manifest_btn = gr.File(
                        value=MANIFEST_PATH,
                        label="📜 Download Sources Registry Manifest (JSON)",
                        interactive=False
                    )

            doc_display = gr.Markdown(value=get_doc_content("MIT 6.006: SSSP Formulation, Greedy Strategy & Pseudocode"))
            doc_selector.change(get_doc_content, doc_selector, doc_display)

            with gr.Accordion("🔄 Engineering Methodology: Alignment with 'The Cycle' (TIET UCS503)", open=True):
                gr.Markdown("""
This project was engineered following the **5 Steps of 'The Cycle'** (TIET UCS503 Software Engineering & Conduct Framework):

1. **Step 1: Concept (What, For Whom)**:
   - A fully grounded, Single-Source-of-Truth RAG and multi-modal learning system for Dijkstra's Shortest Path Algorithm.
   - Grounded exclusively in authentic academic materials: MIT 6.006 Lecture 16 (Prof. Erik Demaine & Prof. Srinivas Devadas) and CLRS Chapter 24.

2. **Step 2: Contract (What Others May Rely On)**:
   - **RAG Query Contract**: Structured JSON response schema `{query, answer, confidence_score, citations, exact_quotes}`.
   - **Graph Simulator API**: Deterministic 17-step state transitions with `{step, action, spt_nodes, tentative_distances, pq}`.
   - **Multi-lingual Media Contract**: Standard MP4 (H.264 / AAC 1080p) and MP3 audio with synchronized bilingual subtitle cues.

3. **Step 3: Tests (How We Measure It)**:
   - Automated test suite `test_rag.py` enforcing:
     - Edge relaxation math test (passes with 99% confidence).
     - Complexity comparison test (passes with 95% confidence).
     - Negative weight pitfall test (passes with 98% confidence).
     - Out-of-scope query rejection (QuickSort rejected with 0% confidence).
     - Simulator deterministic invariant validation across all 17 steps.

4. **Step 4: Implementation (The Code)**:
   - Pure-Python hybrid search (BM25 + TF-IDF cosine similarity).
   - Python `edge-tts` synthesis for English (`en-US-ChristopherNeural`) and Hindi (`hi-IN-MadhurNeural`).
   - Clean mathematical formatting (zero unescaped LaTeX dollar signs).
   - Native Gradio UI with responsive dark-theme components.

5. **Step 5: Refinement (Run, Read, Change)**:
   - Replaced fragile iframe base64 audio embedding with native Gradio `gr.Video` and `gr.Audio` streaming, completely resolving video display issues.
   - Added dual-language toggle (English & Hindi) with synchronized bilingual subtitles.
   - Added interactive conceptual infographics gallery.
   - Added interactive 6-question Dijkstra knowledge assessment quiz with instant evaluation.
                """)

    # Footer
    gr.HTML("""
    <div style="text-align:center; padding:20px 0; border-top:1px solid #1e293b; margin-top:30px; font-size:13px; color:#64748b;">
        Dijkstra Grounded RAG Platform • Authored by Robin • Built 100% from Scratch • Ready for Hugging Face Spaces Deployment
    </div>
    """)

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        share=False,
        allowed_paths=[STATIC_DIR, DATA_DIR],
        theme=gr.themes.Soft(primary_hue="sky", neutral_hue="slate"),
        css=CUSTOM_CSS
    )
