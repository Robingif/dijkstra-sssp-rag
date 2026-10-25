# GeeksforGeeks: Dijkstra's Shortest Path Algorithm (Adjacency Matrix Representation)

**Source**: GeeksforGeeks (https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/)  
**Topic**: Single Source Shortest Path (SSSP) in Weighted Graphs  
**Complexity**: Time: O(V²), Space: O(V)  
**Applicability**: Dense Graphs, Non-negative edge weights  

---

## 1. Overview and Problem Definition

Given a weighted graph and a designated source vertex `src` in the graph, find the shortest paths from the source to all other vertices in the given graph.

- **Input**: Graph G = (V, E), edge weight function w: E → \mathbb{R_{≥ 0, and source vertex s in V.
- **Condition**: All edge weights must be non-negative: for all (u, v) in E, w(u, v) ≥ 0.
- **Output**: An array `dist[]` where `dist[v]` is the shortest path distance from `src` to `v`.

---

## 2. Algorithm Concept and Greedy Strategy

Dijkstra's algorithm is a **greedy algorithm** that generates a **Shortest Path Tree (SPT)** with the given source as the root. It maintains two sets of vertices:
1. **SPT Set (`visited[]` or `sptSet[]`)**: Vertices whose shortest distance from the source is already calculated and finalized.
2. **Unprocessed Set**: Vertices whose shortest distance is not yet finalized.

At every step of the algorithm:
1. Find a vertex `u` that is **not yet in `sptSet`** and has the **minimum tentative distance** `dist[u]`.
2. Include this vertex `u` into `sptSet`.
3. **Relax** all adjacent vertices `v` of `u`:
   
```
If  v \notin sptSet and  dist[u] ≠ ∞  and  dist[u] + weight(u, v) < dist[v]:
```

   
```
dist[v] = dist[u] + weight(u, v)
```


---

## 3. Step-by-Step Example (9 Vertices)

Consider a graph with 9 vertices (0 to 8) represented as an adjacency matrix:
- Vertices: `0, 1, 2, 3, 4, 5, 6, 7, 8`
- Source vertex: `0`

### Initial State:
- `dist = [0, inf, inf, inf, inf, inf, inf, inf, inf]`
- `sptSet = [False, False, False, False, False, False, False, False, False]`

### Step 1:
- Pick vertex with min dist: `u = 0` (`dist[0] = 0`).
- Mark `sptSet[0] = True`.
- Neighbors of 0:
  - Edge (0, 1) with weight 4: `dist[1] = min(inf, 0 + 4) = 4`
  - Edge (0, 7) with weight 8: `dist[7] = min(inf, 0 + 8) = 8`
- `dist = [0, 4, inf, inf, inf, inf, inf, 8, inf]`

### Step 2:
- Pick vertex with min dist not in `sptSet`: `u = 1` (`dist[1] = 4`).
- Mark `sptSet[1] = True`.
- Relax neighbors of 1:
  - Edge (1, 2) weight 8: `dist[2] = min(inf, 4 + 8) = 12`
  - Edge (1, 7) weight 11: `dist[7] = min(8, 4 + 11) = 8` (no change)

### Repeating until all vertices are in `sptSet`:
- Final `dist[]` array:
  - `dist[0] = 0`
  - `dist[1] = 4`
  - `dist[2] = 12`
  - `dist[3] = 19`
  - `dist[4] = 21`
  - `dist[5] = 11`
  - `dist[6] = 9`
  - `dist[7] = 8`
  - `dist[8] = 14`

---

## 4. Complete Implementation in Python

```python
import sys

class DijkstraMatrix:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

    def min_distance(self, dist, spt_set):
        """Find the vertex with minimum distance value from the set of vertices not yet in spt_set"""
        min_val = sys.maxsize
        min_index = -1
        for u in range(self.V):
            if dist[u] < min_val and not spt_set[u]:
                min_val = dist[u]
                min_index = u
        return min_index

    def dijkstra(self, src):
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        spt_set = [False] * self.V
        parent = [-1] * self.V

        for _ in range(self.V):
            u = self.min_distance(dist, spt_set)
            if u == -1:
                break
            spt_set[u] = True

            for v in range(self.V):
                if (self.graph[u][v] > 0 and 
                    not spt_set[v] and 
                    dist[u] + self.graph[u][v] < dist[v]):
                    dist[v] = dist[u] + self.graph[u][v]
                    parent[v] = u

        return dist, parent
```

---

## 5. Complexity Analysis

1. **Time Complexity**:
   - The outer loop runs V times.
   - Inside the loop, `min_distance()` linearly scans V vertices: O(V).
   - Updating distances to adjacent vertices takes O(V) time.
   - Total Time: V × (O(V) + O(V)) = O(V²).
   - For dense graphs where E ≈ V², O(V²) is optimal.

2. **Space Complexity**:
   - Adjacency matrix: O(V²).
   - `dist[]` and `sptSet[]` arrays: O(V).
   - Total Space: O(V²) (or O(V) auxiliary if graph is pre-existing).
