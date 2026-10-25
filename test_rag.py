import os
import rag_engine
import graph_simulator
import quiz_engine
import interactive_visuals

def run_tests():
    print("=" * 65)
    print("RUNNING COMPLETE DIJKSTRA PLATFORM VERIFICATION SUITE")
    print("Aligned with 'The Cycle' (TIET UCS503 Software Engineering Standards)")
    print("=" * 65)

    # 1. Initialize RAG engine
    engine = rag_engine.HybridRAGEngine("data")
    print(f"[OK] RAG Engine initialized: {len(engine.chunks)} indexed chunks.")

    # 2. Test Core Queries
    test_queries = [
        ("Time Complexity", "What is the time complexity of Dijkstra using Adjacency Matrix vs Min-Heap?"),
        ("Negative Weights", "Why does Dijkstra fail on graphs with negative edge weights?"),
        ("MIT 6.006 Edge Relaxation", "Explain the edge relaxation step and triangle inequality in MIT 6.006."),
        ("Real-World Applications", "How does OSPF internet routing use Dijkstra's algorithm?"),
        ("Out-of-Scope Guardrail", "How does quicksort partition an array?")
    ]

    for name, q in test_queries:
        print(f"\n--- Testing: {name} ---")
        print(f"Query: '{q}'")
        res = engine.answer_query(q)
        print(f"Grounded: {res['is_grounded']} | Confidence: {res['confidence']}%")
        print(f"Citations count: {len(res['citations'])}")
        safe_snippet = res['answer'][:120].encode('ascii', errors='replace').decode('ascii')
        print(f"Answer snippet: {safe_snippet}...")

    # 3. Test Graph Simulator
    sim = graph_simulator.DijkstraSimulator()
    print(f"\n[OK] Graph Simulator initialized: {sim.get_total_steps()} simulation steps.")
    step0 = sim.get_step_data(0)
    print(f"Step 0: {step0['action']}")
    step_final = sim.get_step_data(sim.get_total_steps() - 1)
    print(f"Final Step: {step_final['action']}")

    # 4. Test Quiz Engine
    print("\n--- Testing Quiz Engine ---")
    mock_perfect_answers = {
        q["id"]: q["options"][q["correct_idx"]]
        for q in quiz_engine.QUIZ_QUESTIONS
    }
    correct_count, total, percentage, badge, review_items = quiz_engine.evaluate_quiz(mock_perfect_answers)
    print(f"[OK] Quiz Perfect Test: {correct_count}/{total} ({percentage}%) - {badge.encode('ascii', errors='replace').decode('ascii')}")
    assert correct_count == total, "Perfect quiz answers must yield 100% score"

    # 5. Test Interactive Visuals
    print("\n--- Testing Interactive Visuals Gallery ---")
    visuals_html = interactive_visuals.get_all_interactive_visuals_html()
    print(f"[OK] Visuals Gallery generated: {len(visuals_html)} characters.")
    assert "Visual 1: Edge Relaxation" in visuals_html
    assert "Visual 2: The 3-Node Counterexample" in visuals_html

    # 6. Verify Deliverables on Disk
    deliverables = [
        ("PowerPoint Presentation", "static/Dijkstra_Algorithm_Complete_Guide.pptx"),
        ("Interactive HTML Slides", "static/slides.html"),
        ("English Voice-Over Audio", "static/dijkstra_voiceover_english.mp3"),
        ("Hindi Voice-Over Audio", "static/dijkstra_voiceover_hindi.mp3"),
        ("English Walkthrough Video (MP4)", "static/dijkstra_walkthrough_english.mp4"),
        ("Hindi Walkthrough Video (MP4)", "static/dijkstra_walkthrough_hindi.mp4"),
        ("Official MIT Lecture 16 PDF", "data/archive/MIT6_006F11_lec16.pdf"),
        ("Sources Registry Manifest", "data/archive/sources_manifest.json")
    ]

    print("\n--- Verifying All Multi-Modal Deliverables ---")
    all_found = True
    for label, path in deliverables:
        if os.path.exists(path):
            size_kb = os.path.getsize(path) / 1024
            print(f"[OK] {label}: {path} ({size_kb:.1f} KB)")
        else:
            print(f"[FAIL MISSING]: {path}")
            all_found = False

    assert all_found, "All deliverables must exist on disk!"

    print("\n" + "=" * 65)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY WITH ZERO ERRORS!")
    print("=" * 65)

if __name__ == "__main__":
    run_tests()
