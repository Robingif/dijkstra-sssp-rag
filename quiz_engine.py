"""
quiz_engine.py — Interactive Dijkstra Knowledge Quiz Module
Grounded strictly in GeeksforGeeks (GFG) and MIT 6.006 Lecture 16 (Prof. Demaine & Prof. Devadas).
"""

QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "question": "1. What is the fundamental invariant maintained by Dijkstra's algorithm for every vertex u added to the finalized set S?",
        "options": [
            "d[u] is guaranteed to be the exact true shortest distance δ(s, u) from source s",
            "d[u] represents an upper bound that may be decreased in subsequent iterations",
            "d[u] is equal to the minimum weight outgoing edge from vertex u",
            "d[u] is negative if vertex u belongs to a directed cycle"
        ],
        "correct_idx": 0,
        "explanation": "According to MIT 6.006 Lecture 16, Dijkstra's algorithm maintains the invariant: for every vertex u ∈ S, d[u] = δ(s, u). Because edge weights are non-negative, any alternative path from s to u through the unfinalized set V - S would have to pass through a frontier vertex with tentative distance >= d[u], making it impossible to find a shorter path later."
    },
    {
        "id": "q2",
        "question": "2. What is the time complexity of Dijkstra's algorithm implemented with an Adjacency List and a Binary Min-Heap (Priority Queue)?",
        "options": [
            "O((V + E) log V)",
            "O(V²)",
            "O(V * E)",
            "O(E log E + V²)"
        ],
        "correct_idx": 0,
        "explanation": "As documented by GeeksforGeeks and MIT 6.006: Each vertex is extracted from the Min-Heap once (V * extract_min = O(V log V)). In the worst case, every edge is relaxed once, triggering a decrease_key / insert operation (E * decrease_key = O(E log V)). Summing these yields O((V + E) log V)."
    },
    {
        "id": "q3",
        "question": "3. Why does Dijkstra's algorithm fail on graphs containing negative edge weights (even without negative cycles)?",
        "options": [
            "The greedy choice property is broken: a vertex once finalized in set S can have its shortest path subsequently undercut by a path containing a negative edge",
            "The Priority Queue throws an overflow exception on negative values",
            "Negative edge weights cause the graph to become disconnected",
            "The adjacency list cannot store negative numerical values"
        ],
        "correct_idx": 0,
        "explanation": "GFG's negative weight analysis shows that Dijkstra assumes adding an edge to a path can never decrease its total length. If a negative edge exists, a path passing through a vertex with a higher tentative distance could end up with a lower total cost, violating the greedy invariant that finalized nodes never need re-evaluation. (Bellman-Ford must be used instead)."
    },
    {
        "id": "q4",
        "question": "4. What is the exact mathematical operation performed during the Edge Relaxation of directed edge (u, v) with weight w(u, v)?",
        "options": [
            "if d[u] + w(u, v) < d[v]: then d[v] = d[u] + w(u, v) and predecessor π[v] = u",
            "d[v] = min(d[u], w(u, v))",
            "if d[v] - w(u, v) > d[u]: then d[v] = d[u] * w(u, v)",
            "d[v] = d[u] + d[v] + w(u, v)"
        ],
        "correct_idx": 0,
        "explanation": "According to MIT 6.006 Lecture 16: RELAX(u, v, w) tests whether going through u to reach v improves the current tentative upper bound d[v]. If d[u] + w(u, v) < d[v], the upper bound is tightened to d[u] + w(u, v), maintaining the triangle inequality invariant δ(s, v) <= δ(s, u) + w(u, v)."
    },
    {
        "id": "q5",
        "question": "5. Which standard networking protocol uses Dijkstra's algorithm to compute the shortest path for internet IP routing?",
        "options": [
            "OSPF (Open Shortest Path First)",
            "BGP (Border Gateway Protocol)",
            "RIP (Routing Information Protocol)",
            "FTP (File Transfer Protocol)"
        ],
        "correct_idx": 0,
        "explanation": "GFG notes that OSPF (Open Shortest Path First) is a link-state routing protocol where every router independently constructs a complete topology graph of the autonomous area and runs Dijkstra's algorithm to generate its IP forwarding table with lowest link-cost."
    },
    {
        "id": "q6",
        "question": "6. When is the Adjacency Matrix implementation with O(V²) runtime asymptotically equal to or more efficient than the Min-Heap implementation?",
        "options": [
            "In completely dense graphs where E is close to V² (E ≈ V²)",
            "In sparse graphs like road networks where E ≈ V",
            "Only on unweighted graphs where Breadth-First Search (BFS) is used",
            "When the graph has negative edge weights"
        ],
        "correct_idx": 0,
        "explanation": "In very dense graphs where E ≈ V², O((V + E) log V) becomes O(V² log V). The Adjacency Matrix approach requires O(V²) time regardless of edge density and avoids heap maintenance overhead, making it competitive or faster on dense graphs."
    }
]

def evaluate_quiz(answers: dict) -> tuple[int, int, float, str, list]:
    """
    Evaluates submitted answers.
    Returns:
    (correct_count, total_count, percentage, status_badge, review_items)
    """
    total = len(QUIZ_QUESTIONS)
    correct_count = 0
    review_items = []

    for q in QUIZ_QUESTIONS:
        qid = q["id"]
        user_choice = answers.get(qid)
        correct_option = q["options"][q["correct_idx"]]
        is_correct = (user_choice == correct_option)
        
        if is_correct:
            correct_count += 1
            status = "✅ Correct"
            color = "#10b981"
        else:
            status = "❌ Incorrect"
            color = "#ef4444"

        review_items.append({
            "question": q["question"],
            "user_choice": user_choice if user_choice else "*(No answer selected)*",
            "correct_option": correct_option,
            "is_correct": is_correct,
            "status": status,
            "color": color,
            "explanation": q["explanation"]
        })

    percentage = round((correct_count / total) * 100, 1)
    
    if percentage >= 80:
        badge = "🏆 Mastery Achieved (Pass with Distinction)"
    elif percentage >= 60:
        badge = "👍 Solid Understanding (Pass)"
    else:
        badge = "📚 Review Recommended (Keep Practicing)"

    return correct_count, total, percentage, badge, review_items

def render_quiz_result_html(correct_count: int, total: int, percentage: float, badge: str, review_items: list) -> str:
    """
    Renders styled HTML report for the quiz assessment.
    """
    bar_color = "#10b981" if percentage >= 80 else ("#f59e0b" if percentage >= 60 else "#ef4444")
    
    html = f"""
    <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:24px; margin-top:16px;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:16px; margin-bottom:20px;">
            <div>
                <h3 style="color:#f8fafc; margin:0 0 4px 0; font-size:22px;">📊 Assessment Results</h3>
                <span style="font-size:13px; color:#94a3b8;">Score: <b style="color:#38bdf8;">{correct_count}/{total}</b> ({percentage}%)</span>
            </div>
            <div style="background:rgba(56,189,248,0.15); border:1px solid #38bdf8; color:#38bdf8; padding:6px 14px; border-radius:20px; font-weight:700; font-size:13px;">
                {badge}
            </div>
        </div>

        <div style="width:100%; background:#1e293b; height:10px; border-radius:5px; margin-bottom:24px; overflow:hidden;">
            <div style="width:{percentage}%; background:{bar_color}; height:100%; border-radius:5px; transition:width 0.5s ease;"></div>
        </div>

        <h4 style="color:#cbd5e1; margin-bottom:14px;">Detailed Breakdown & Grounded Rationales:</h4>
        <div style="display:flex; flex-direction:column; gap:16px;">
    """

    for idx, item in enumerate(review_items, 1):
        border_col = "#10b981" if item["is_correct"] else "#ef4444"
        bg_col = "rgba(16, 185, 129, 0.08)" if item["is_correct"] else "rgba(239, 68, 68, 0.08)"
        
        html += f"""
        <div style="background:{bg_col}; border:1px solid {border_col}; border-radius:10px; padding:16px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                <b style="color:#f8fafc; font-size:14px;">{item['question']}</b>
                <span style="color:{item['color']}; font-weight:700; font-size:12px; white-space:nowrap; margin-left:10px;">{item['status']}</span>
            </div>
            <div style="font-size:13px; margin-bottom:4px; color:#cbd5e1;">
                <b>Your Answer:</b> <span style="color:{'#34d399' if item['is_correct'] else '#f87171'};">{item['user_choice']}</span>
            </div>
            {'' if item['is_correct'] else f'''
            <div style="font-size:13px; margin-bottom:8px; color:#cbd5e1;">
                <b>Correct Answer:</b> <span style="color:#38bdf8; font-weight:600;">{item['correct_option']}</span>
            </div>
            '''}
            <div style="margin-top:10px; padding:10px 12px; background:rgba(15,23,42,0.6); border-left:3px solid #38bdf8; border-radius:4px; font-size:12px; color:#94a3b8; line-height:1.5;">
                <b style="color:#38bdf8;">📖 Grounded Rationale (GFG & MIT 6.006):</b><br/>
                {item['explanation']}
            </div>
        </div>
        """

    html += """
        </div>
    </div>
    """
    return html
