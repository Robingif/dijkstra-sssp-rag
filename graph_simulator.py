import heapq
from typing import Dict, List, Tuple, Any

class DijkstraSimulator:
    def __init__(self):
        # Default 6-node weighted graph from GeeksforGeeks & MIT lecture
        # Vertices: 0=A, 1=B, 2=C, 3=D, 4=E, 5=F
        self.node_labels = ["A", "B", "C", "D", "E", "F"]
        self.node_positions = {
            0: (120, 200),  # A (Source)
            1: (280, 100),  # B
            2: (280, 300),  # C
            3: (480, 100),  # D
            4: (480, 300),  # E
            5: (640, 200),  # F (Target)
        }
        self.edges = [
            (0, 1, 4),  # A -> B (4)
            (0, 2, 2),  # A -> C (2)
            (1, 2, 1),  # B -> C (1)
            (1, 3, 5),  # B -> D (5)
            (2, 4, 8),  # C -> E (8)
            (2, 3, 10), # C -> D (10)
            (3, 4, 2),  # D -> E (2)
            (3, 5, 6),  # D -> F (6)
            (4, 5, 3),  # E -> F (3)
        ]
        self.V = len(self.node_labels)
        self.adj = self._build_adj()
        self.steps = []
        self._record_simulation(src=0)

    def _build_adj(self) -> List[List[Tuple[int, int]]]:
        adj = [[] for _ in range(self.V)]
        for u, v, w in self.edges:
            adj[u].append((v, w))
            adj[v].append((u, w))  # Undirected
        return adj

    def _record_simulation(self, src: int = 0):
        self.steps = []
        dist = [float('inf')] * self.V
        parent = [-1] * self.V
        visited = [False] * self.V
        dist[src] = 0

        pq = [(0, src)]
        
        # Initial step
        self.steps.append({
            "step_num": 0,
            "action": f"Initialize: Set dist[{self.node_labels[src]}] = 0, all other distances = inf. Insert ({self.node_labels[src]}, 0) into Priority Queue.",
            "current_node": src,
            "active_edge": None,
            "dist": list(dist),
            "visited": list(visited),
            "pq": [(d, self.node_labels[node]) for d, node in pq],
            "tree_edges": []
        })

        step_counter = 1
        tree_edges = []

        while pq:
            current_dist, u = heapq.heappop(pq)
            if visited[u]:
                continue
            
            visited[u] = True
            u_label = self.node_labels[u]

            self.steps.append({
                "step_num": step_counter,
                "action": f"Extract-Min: Pick vertex {u_label} with minimum tentative distance {current_dist}. Finalize {u_label}.",
                "current_node": u,
                "active_edge": None,
                "dist": list(dist),
                "visited": list(visited),
                "pq": [(d, self.node_labels[node]) for d, node in pq if not visited[node]],
                "tree_edges": list(tree_edges)
            })
            step_counter += 1

            for v, weight in sorted(self.adj[u], key=lambda x: x[0]):
                v_label = self.node_labels[v]
                if not visited[v]:
                    new_dist = dist[u] + weight
                    old_dist = dist[v]
                    if new_dist < old_dist:
                        dist[v] = new_dist
                        parent[v] = u
                        heapq.heappush(pq, (new_dist, v))
                        
                        # Update tree edge
                        tree_edges = [e for e in tree_edges if e[1] != v]
                        tree_edges.append((u, v))

                        self.steps.append({
                            "step_num": step_counter,
                            "action": f"Relax edge ({u_label}, {v_label}): Distance to {v_label} updated from {'inf' if old_dist == float('inf') else old_dist} to {new_dist} ({dist[u]} + {weight}). Push ({v_label}, {new_dist}) to PQ.",
                            "current_node": u,
                            "active_edge": (u, v),
                            "dist": list(dist),
                            "visited": list(visited),
                            "pq": [(d, self.node_labels[node]) for d, node in sorted(pq) if not visited[node]],
                            "tree_edges": list(tree_edges)
                        })
                        step_counter += 1
                    else:
                        self.steps.append({
                            "step_num": step_counter,
                            "action": f"Examine edge ({u_label}, {v_label}): New path ({dist[u]} + {weight} = {new_dist}) is NOT shorter than existing dist[{v_label}] = {old_dist}. No change.",
                            "current_node": u,
                            "active_edge": (u, v),
                            "dist": list(dist),
                            "visited": list(visited),
                            "pq": [(d, self.node_labels[node]) for d, node in sorted(pq) if not visited[node]],
                            "tree_edges": list(tree_edges)
                        })
                        step_counter += 1

        # Final completion step
        self.steps.append({
            "step_num": step_counter,
            "action": f"Complete: Priority Queue is empty. All reachable vertices finalized. Shortest Path Tree successfully constructed!",
            "current_node": None,
            "active_edge": None,
            "dist": list(dist),
            "visited": list(visited),
            "pq": [],
            "tree_edges": list(tree_edges)
        })

    def get_total_steps(self) -> int:
        return len(self.steps)

    def get_step_data(self, step_idx: int) -> Dict[str, Any]:
        idx = max(0, min(step_idx, len(self.steps) - 1))
        return self.steps[idx]

    def render_svg(self, step_idx: int) -> str:
        step = self.get_step_data(step_idx)
        current_node = step["current_node"]
        active_edge = step["active_edge"]
        dist = step["dist"]
        visited = step["visited"]
        tree_edges = step["tree_edges"]

        svg_width, svg_height = 760, 420
        svg = [f'<svg width="100%" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:12px; font-family:system-ui, -apple-system, sans-serif;">']
        
        # Defs for glow filters and markers
        svg.append('''
        <defs>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <linearGradient id="treeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#10b981" />
                <stop offset="100%" stop-color="#059669" />
            </linearGradient>
        </defs>
        ''')

        # 1. Draw Edges
        for u, v, w in self.edges:
            x1, y1 = self.node_positions[u]
            x2, y2 = self.node_positions[v]
            
            # Check edge state
            is_active = (active_edge == (u, v) or active_edge == (v, u))
            is_tree = (u, v) in tree_edges or (v, u) in tree_edges

            stroke_color = "#334155"
            stroke_width = 2
            dash_array = "none"

            if is_tree:
                stroke_color = "#10b981"  # Emerald
                stroke_width = 4
            if is_active:
                stroke_color = "#f59e0b"  # Amber
                stroke_width = 5
                dash_array = "6,4"

            svg.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke_color}" stroke-width="{stroke_width}" stroke-dasharray="{dash_array}" />')

            # Weight badge at midpoint
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            # Offset slightly to prevent collision with line
            dx, dy = -(y2 - y1), (x2 - x1)
            dist_len = (dx*dx + dy*dy)**0.5
            if dist_len > 0:
                off_x = mx + int(14 * dx / dist_len)
                off_y = my + int(14 * dy / dist_len)
            else:
                off_x, off_y = mx, my - 10

            badge_bg = "#f59e0b" if is_active else ("#047857" if is_tree else "#1e293b")
            svg.append(f'<rect x="{off_x-12}" y="{off_y-10}" width="24" height="20" rx="4" fill="{badge_bg}" stroke="#475569" stroke-width="1"/>')
            svg.append(f'<text x="{off_x}" y="{off_y+4}" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">{w}</text>')

        # 2. Draw Nodes
        for i in range(self.V):
            x, y = self.node_positions[i]
            label = self.node_labels[i]
            d_val = "∞" if dist[i] == float('inf') else str(dist[i])
            is_vis = visited[i]
            is_curr = (current_node == i)

            # Node Fill & Stroke colors
            if is_curr:
                node_fill = "#f59e0b"  # Amber glow
                node_stroke = "#fbbf24"
                stroke_w = 4
                filter_str = 'filter="url(#glow)"'
            elif is_vis:
                node_fill = "#10b981"  # Finalized Green
                node_stroke = "#34d399"
                stroke_w = 3
                filter_str = ""
            else:
                node_fill = "#1e293b"  # Unvisited Dark Slate
                node_stroke = "#64748b"
                stroke_w = 2
                filter_str = ""

            # Main Node Circle
            svg.append(f'<circle cx="{x}" cy="{y}" r="26" fill="{node_fill}" stroke="{node_stroke}" stroke-width="{stroke_w}" {filter_str} />')
            svg.append(f'<text x="{x}" y="{y+6}" fill="#ffffff" font-size="16" font-weight="bold" text-anchor="middle">{label}</text>')

            # Distance pill above node
            dist_pill_bg = "#f59e0b" if is_curr else ("#10b981" if is_vis else "#334155")
            svg.append(f'<rect x="{x-26}" y="{y-44}" width="52" height="18" rx="9" fill="{dist_pill_bg}" />')
            svg.append(f'<text x="{x}" y="{y-31}" fill="#ffffff" font-size="11" font-weight="bold" text-anchor="middle">d={d_val}</text>')

        # 3. Legend & Step Header
        svg.append(f'<text x="20" y="32" fill="#94a3b8" font-size="13" font-weight="600">STEP {step["step_num"]} / {len(self.steps)-1}</text>')
        
        # Legend items
        legend_items = [
            ("#f59e0b", "Current Min / Active"),
            ("#10b981", "Finalized (In SPT)"),
            ("#1e293b", "Unvisited"),
            ("#10b981", "SPT Edge")
        ]
        leg_x = 220
        for color, text in legend_items:
            svg.append(f'<circle cx="{leg_x}" cy="28" r="6" fill="{color}" stroke="#64748b" stroke-width="1"/>')
            svg.append(f'<text x="{leg_x+12}" y="32" fill="#cbd5e1" font-size="11">{text}</text>')
            leg_x += 130

        # Action banner at bottom
        action_text = step["action"]
        if len(action_text) > 95:
            action_text = action_text[:92] + "..."
        svg.append(f'<rect x="15" y="{svg_height-48}" width="{svg_width-30}" height="36" rx="8" fill="#1e293b" stroke="#334155"/>')
        svg.append(f'<text x="28" y="{svg_height-25}" fill="#38bdf8" font-size="13" font-family="monospace">▶ {action_text}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    def render_distance_table_html(self, step_idx: int) -> str:
        step = self.get_step_data(step_idx)
        dist = step["dist"]
        visited = step["visited"]

        html = ['<div style="overflow-x:auto;"><table style="width:100%; border-collapse:collapse; font-size:13px; text-align:center;">']
        html.append('<tr style="background:#1e293b; color:#94a3b8; border-bottom:1px solid #334155;">')
        html.append('<th style="padding:8px;">Vertex</th>')
        for label in self.node_labels:
            html.append(f'<th style="padding:8px;">{label}</th>')
        html.append('</tr>')

        # Distance row
        html.append('<tr style="background:#0f172a; border-bottom:1px solid #334155;">')
        html.append('<td style="padding:8px; font-weight:bold; color:#38bdf8;">d[v]</td>')
        for d in dist:
            val = "∞" if d == float('inf') else str(d)
            html.append(f'<td style="padding:8px; font-weight:600; color:#f8fafc;">{val}</td>')
        html.append('</tr>')

        # Status row
        html.append('<tr style="background:#0f172a;">')
        html.append('<td style="padding:8px; font-weight:bold; color:#94a3b8;">Status</td>')
        for vis in visited:
            badge = '<span style="color:#10b981; font-weight:bold;">Finalized</span>' if vis else '<span style="color:#64748b;">Pending</span>'
            html.append(f'<td style="padding:8px;">{badge}</td>')
        html.append('</tr>')

        html.append('</table></div>')
        return "\n".join(html)

    def render_pq_html(self, step_idx: int) -> str:
        step = self.get_step_data(step_idx)
        pq = step["pq"]
        if not pq:
            return '<div style="color:#94a3b8; font-style:italic; padding:8px;">Priority Queue is empty.</div>'
        
        badges = []
        for d, node_label in pq:
            badges.append(f'<span style="display:inline-block; background:#1e293b; border:1px solid #3b82f6; border-radius:6px; padding:4px 10px; margin:3px; color:#f8fafc; font-family:monospace; font-size:12px;"><b>{node_label}</b>: {d}</span>')
        return f'<div style="padding:6px 0;">{" ".join(badges)}</div>'
