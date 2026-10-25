"""
interactive_visuals.py — Animated Interactive Photos and Infographics for Dijkstra's Algorithm
Features animated SVGs, CSS micro-interactions, hover glow effects, and comparative architecture cards.
"""

def get_relaxation_card_html() -> str:
    return """
    <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="margin:0; color:#38bdf8; font-size:16px;">🔍 Visual 1: Edge Relaxation Mechanism (d[u] + w(u,v) < d[v])</h4>
            <span style="background:rgba(56,189,248,0.15); border:1px solid #38bdf8; color:#38bdf8; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700;">MIT 6.006 RELAX Invariant</span>
        </div>
        <p style="font-size:13px; color:#94a3b8; margin-bottom:16px;">
            Hover over the graph to trigger the animated relaxation process. Notice how the tentative distance of node <b>V</b> drops from 8 to 5 because path through <b>U</b> offers a strictly shorter route (2 + 3 = 5 < 8).
        </p>

        <div style="background:#0b0f19; border:1px solid #1e293b; border-radius:10px; padding:15px; display:flex; justify-content:center; align-items:center;">
            <svg width="680" height="220" viewBox="0 0 680 220" style="background:#0b0f19; overflow:visible;">
                <defs>
                    <linearGradient id="relEdgeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#f59e0b" />
                        <stop offset="100%" stop-color="#10b981" />
                    </linearGradient>
                    <filter id="glowEffect">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feComposite in="SourceGraphic" in2="blur" operator="over" />
                    </filter>
                </defs>

                <!-- Source to U -->
                <line x1="80" y1="110" x2="260" y2="70" stroke="#10b981" stroke-width="4" stroke-dasharray="6,4" />
                <text x="165" y="75" fill="#34d399" font-size="12" font-weight="bold">w=2 (Shortest)</text>

                <!-- Direct Source to V (older sub-optimal) -->
                <line x1="80" y1="110" x2="480" y2="150" stroke="#ef4444" stroke-width="2" opacity="0.5" />
                <text x="260" y="150" fill="#f87171" font-size="12">Old direct path = 8</text>

                <!-- Relaxation Edge: U -> V -->
                <line x1="260" y1="70" x2="480" y2="150" stroke="url(#relEdgeGrad)" stroke-width="4" />
                <circle cx="370" cy="110" r="14" fill="#0f172a" stroke="#f59e0b" stroke-width="2"/>
                <text x="370" y="115" fill="#f59e0b" font-size="12" font-weight="bold" text-anchor="middle">w=3</text>

                <!-- Node S (Source) -->
                <g transform="translate(80, 110)">
                    <circle r="26" fill="#1e293b" stroke="#38bdf8" stroke-width="3" filter="url(#glowEffect)"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">S</text>
                    <text y="42" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">d[S]=0</text>
                </g>

                <!-- Node U -->
                <g transform="translate(260, 70)">
                    <circle r="26" fill="#10b981" stroke="#34d399" stroke-width="3"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">U</text>
                    <text y="-35" fill="#34d399" font-size="12" font-weight="bold" text-anchor="middle">d[U] = 2 (Fixed)</text>
                </g>

                <!-- Node V -->
                <g transform="translate(480, 150)">
                    <circle r="26" fill="#f59e0b" stroke="#fbbf24" stroke-width="3"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">V</text>
                    <text y="42" fill="#fbbf24" font-size="12" font-weight="bold" text-anchor="middle">d[V]: 8 ➔ 5 (Relaxed!)</text>
                </g>

                <!-- Status Card on right -->
                <g transform="translate(540, 40)">
                    <rect width="130" height="130" rx="8" fill="#1e293b" stroke="#334155" />
                    <text x="65" y="24" fill="#38bdf8" font-size="11" font-weight="bold" text-anchor="middle">RELAX CONDITION</text>
                    <text x="12" y="50" fill="#94a3b8" font-size="11">d[U] + w(U,V) &lt; d[V]</text>
                    <text x="12" y="72" fill="#34d399" font-size="11" font-weight="bold">2 + 3 &lt; 8 (TRUE)</text>
                    <text x="12" y="96" fill="#fbbf24" font-size="11">d[V] = 5</text>
                    <text x="12" y="116" fill="#38bdf8" font-size="11">π[V] = U</text>
                </g>
            </svg>
        </div>
    </div>
    """

def get_negative_weights_card_html() -> str:
    return """
    <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="margin:0; color:#ef4444; font-size:16px;">⚠️ Visual 2: The 3-Node Counterexample (Why Dijkstra Fails on Negative Edges)</h4>
            <span style="background:rgba(239,68,68,0.15); border:1px solid #ef4444; color:#ef4444; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700;">Greedy Invariant Violation</span>
        </div>
        <p style="font-size:13px; color:#94a3b8; margin-bottom:16px;">
            Dijkstra assumes paths grow monotonically. Because node <b>A</b> has distance 3 and node <b>B</b> has distance 5, Dijkstra finalizes <b>A</b> first. But the subsequent negative edge (B ➔ A with weight -4) reduces the path to 1, causing Dijkstra to report the wrong answer (3 instead of 1).
        </p>

        <div style="background:#0b0f19; border:1px solid #1e293b; border-radius:10px; padding:15px; display:flex; justify-content:center; align-items:center;">
            <svg width="680" height="230" viewBox="0 0 680 230" style="background:#0b0f19;">
                <defs>
                    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444"/>
                    </marker>
                    <marker id="arrowGreen" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981"/>
                    </marker>
                </defs>

                <!-- Edge S -> A -->
                <line x1="120" y1="120" x2="320" y2="60" stroke="#f59e0b" stroke-width="3" marker-end="url(#arrowGreen)"/>
                <text x="210" y="75" fill="#fbbf24" font-size="13" font-weight="bold">w = 3</text>

                <!-- Edge S -> B -->
                <line x1="120" y1="120" x2="320" y2="180" stroke="#38bdf8" stroke-width="3" marker-end="url(#arrowGreen)"/>
                <text x="210" y="175" fill="#38bdf8" font-size="13" font-weight="bold">w = 5</text>

                <!-- Negative Edge B -> A -->
                <line x1="320" y1="170" x2="320" y2="75" stroke="#ef4444" stroke-width="4" stroke-dasharray="4,3" marker-end="url(#arrow)"/>
                <rect x="260" y="105" width="60" height="24" rx="4" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
                <text x="290" y="122" fill="#ef4444" font-size="12" font-weight="bold" text-anchor="middle">w = -4</text>

                <!-- Node S -->
                <g transform="translate(120, 120)">
                    <circle r="26" fill="#1e293b" stroke="#64748b" stroke-width="3"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">S</text>
                    <text y="42" fill="#94a3b8" font-size="12" font-weight="bold" text-anchor="middle">d=0</text>
                </g>

                <!-- Node A -->
                <g transform="translate(335, 55)">
                    <circle r="26" fill="#1e293b" stroke="#ef4444" stroke-width="3"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">A</text>
                    <text y="-35" fill="#ef4444" font-size="12" font-weight="bold" text-anchor="middle">Dijkstra claims d=3 ❌</text>
                    <text y="-18" fill="#10b981" font-size="12" font-weight="bold" text-anchor="middle">True shortest d=1 ✅</text>
                </g>

                <!-- Node B -->
                <g transform="translate(335, 185)">
                    <circle r="26" fill="#1e293b" stroke="#38bdf8" stroke-width="3"/>
                    <text y="6" fill="#fff" font-size="15" font-weight="bold" text-anchor="middle">B</text>
                    <text y="42" fill="#38bdf8" font-size="12" font-weight="bold" text-anchor="middle">d=5</text>
                </g>

                <!-- Explanatory note -->
                <g transform="translate(430, 35)">
                    <rect width="230" height="150" rx="8" fill="#1e293b" stroke="#334155"/>
                    <text x="115" y="24" fill="#ef4444" font-size="12" font-weight="bold" text-anchor="middle">FATAL GREEDY FAILURE</text>
                    <text x="14" y="52" fill="#cbd5e1" font-size="11">1. Greedy extracts A with d=3</text>
                    <text x="14" y="72" fill="#cbd5e1" font-size="11">2. Node A marked FINALIZED</text>
                    <text x="14" y="92" fill="#cbd5e1" font-size="11">3. Later: Path S➔B➔A has cost:</text>
                    <text x="24" y="112" fill="#34d399" font-size="12" font-weight="bold">5 + (-4) = 1 &lt; 3 !</text>
                    <text x="14" y="134" fill="#f87171" font-size="11">Dijkstra never re-evaluates A!</text>
                </g>
            </svg>
        </div>
    </div>
    """

def get_complexity_card_html() -> str:
    return """
    <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="margin:0; color:#10b981; font-size:16px;">⚡ Visual 3: Adjacency Matrix O(V²) vs Min-Heap O((V+E) log V) Architecture</h4>
            <span style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700;">Data Structure Trade-Off</span>
        </div>
        <p style="font-size:13px; color:#94a3b8; margin-bottom:16px;">
            Comparing memory layout and asymptotic runtimes across graph density topologies.
        </p>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
            <!-- Column 1: Adjacency Matrix -->
            <div style="background:#0b0f19; border:1px solid #334155; border-radius:10px; padding:16px;">
                <div style="color:#f59e0b; font-weight:700; font-size:14px; margin-bottom:8px;">🟦 Adjacency Matrix (Dense Graphs)</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
                    • <b>Data Structure</b>: 2D Array <code>matrix[V][V]</code><br/>
                    • <b>Time Complexity</b>: <code style="color:#f59e0b; font-weight:bold;">O(V²)</code><br/>
                    • <b>Space Complexity</b>: <code style="color:#f59e0b;">O(V²)</code><br/>
                    • <b>Find Min Vertex</b>: Linear scan over <code>V</code> unvisited nodes = <code>O(V)</code><br/>
                    • <b>Relaxation</b>: Check all row elements = <code>O(V)</code><br/>
                    • <b>Best Used For</b>: Dense graphs where <code>E ≈ V²</code> (no priority queue overhead).
                </div>
            </div>

            <!-- Column 2: Min-Heap / Priority Queue -->
            <div style="background:#0b0f19; border:1px solid #334155; border-radius:10px; padding:16px;">
                <div style="color:#38bdf8; font-weight:700; font-size:14px; margin-bottom:8px;">🌲 Min-Heap + Adjacency List (Sparse Graphs)</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.6;">
                    • <b>Data Structure</b>: Binary Heap (e.g. Python <code>heapq</code>)<br/>
                    • <b>Time Complexity</b>: <code style="color:#38bdf8; font-weight:bold;">O((V + E) log V)</code><br/>
                    • <b>Space Complexity</b>: <code style="color:#38bdf8;">O(V + E)</code><br/>
                    • <b>Find Min Vertex</b>: <code>extract_min()</code> = <code>O(log V)</code><br/>
                    • <b>Relaxation</b>: <code>decrease_key()</code> or lazy push = <code>O(log V)</code><br/>
                    • <b>Best Used For</b>: Road networks, Google Maps, GPS, internet topologies (<code>E ≪ V²</code>).
                </div>
            </div>
        </div>
    </div>
    """

def get_spt_card_html() -> str:
    return """
    <div style="background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h4 style="margin:0; color:#a855f7; font-size:16px;">🌐 Visual 4: Shortest Path Tree (SPT) & Frontier Partition (MIT 6.006)</h4>
            <span style="background:rgba(168,85,247,0.15); border:1px solid #a855f7; color:#a855f7; font-size:11px; padding:2px 8px; border-radius:12px; font-weight:700;">Cut Property & Invariant</span>
        </div>
        <p style="font-size:13px; color:#94a3b8; margin-bottom:16px;">
            At any stage during Dijkstra's algorithm, vertices are divided into two disjoint sets: <b>S</b> (finalized shortest paths) and <b>V - S</b> (unvisited / frontier nodes). Because non-negative edges ensure sub-paths only grow, the edge crossing the cut with the minimum tentative value is guaranteed optimal.
        </p>

        <div style="display:flex; gap:16px; align-items:center; background:#0b0f19; border:1px solid #1e293b; border-radius:10px; padding:16px;">
            <div style="flex:1; border-right:1px solid #334155; padding-right:16px;">
                <div style="color:#34d399; font-weight:bold; font-size:13px; margin-bottom:6px;">Finalized Set S (Known δ(s, u)):</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                    • Vertices whose shortest distance is permanently proven.<br/>
                    • Invariant: <code>d[u] = δ(s, u)</code> for all <code>u ∈ S</code>.<br/>
                    • Never modified or popped from the priority queue again.
                </div>
            </div>
            <div style="flex:1; padding-left:8px;">
                <div style="color:#f59e0b; font-weight:bold; font-size:13px; margin-bottom:6px;">Frontier Set V - S (Tentative Bounds):</div>
                <div style="font-size:12px; color:#cbd5e1; line-height:1.5;">
                    • Vertices still in the Min-Heap.<br/>
                    • <code>d[v]</code> is an upper bound on true distance.<br/>
                    • Vertex with <code>min(d[v])</code> across the boundary is safely moved to <code>S</code>.
                </div>
            </div>
        </div>
    </div>
    """

def get_all_interactive_visuals_html() -> str:
    """
    Renders all 4 interactive visual cards into a cohesive gallery.
    """
    return f"""
    <div style="padding:10px 0;">
        {get_relaxation_card_html()}
        {get_negative_weights_card_html()}
        {get_complexity_card_html()}
        {get_spt_card_html()}
    </div>
    """
