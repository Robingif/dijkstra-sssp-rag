# MIT 6.006: Introduction to Algorithms — Lecture 16: Dijkstra's Algorithm

**Instructors**: Prof. Erik Demaine & Prof. Srinivas Devadas  
**Institution**: Massachusetts Institute of Technology (MIT OpenCourseWare)  
**Course**: 6.006 Introduction to Algorithms, Fall 2011  
**Resource URL**: https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/mit6_006f11_lec16/  
**Video Reference**: https://www.youtube.com/watch?v=2E7MmKv0Y24  

---

## 1. Lecture Context and Overview

Prof. Erik Demaine and Prof. Srinivas Devadas present the general framework for Single-Source Shortest Paths (SSSP) on weighted directed graphs G = (V, E, w).

### Core Definitions:
- **Path Weight**: For path p = \langle v_0, v_1, \dots, v_k \rangle:
  
```
w(p) = sum_{i=1^k w(v_{i-1, v_i)
```

- **Shortest-Path Weight**:
  
```
δ(s, v) = \begin{cases \min \{w(p) : s \overset{p{≤adsto v\ & if path exists \\ ∞ & otherwise \end{cases
```

- **Optimal Substructure**: Subpaths of shortest paths are shortest paths. If p = u \overset{p_{uv{≤adsto v \overset{p_{vw{≤adsto w is a shortest path from u to w, then p_{uv is a shortest path from u to v.

---

## 2. The General Edge Relaxation Framework

All shortest-path algorithms in the course maintain two attributes for each vertex v in V:
1. d[v]: Tentative shortest-path estimate (always an upper bound: d[v] ≥ δ(s, v)).
2. π[v]: Predecessor vertex on the shortest path from s to v.

### Initialization (`Initialize-Single-Source(G, s)`):
```text
for each v in V:
    d[v] = infinity
    pi[v] = NIL
d[s] = 0
```

### The Relaxation Step (`Relax(u, v, w)`):
```text
if d[v] > d[u] + w(u, v):
    d[v] = d[u] + w(u, v)
    pi[v] = u
```

### Key Mathematical Invariants of Relaxation:
1. **Upper-Bound Property**: d[v] ≥ δ(s, v) for all v in V at all times. Once d[v] reaches δ(s, v), it never changes.
2. **Triangle Inequality**: For any edge (u, v) in E, δ(s, v) ≤ δ(s, u) + w(u, v).
3. **Convergence Property**: If s ≤adsto u → v is a shortest path, and d[u] = δ(s, u) prior to relaxing edge (u, v), then d[v] = δ(s, v) after the relaxation.
4. **Path-Relaxation Property**: If p = \langle v_0, v_1, \dots, v_k \rangle is a shortest path from s = v_0 to v_k, and edges of p are relaxed in sequence (v_0, v_1), (v_1, v_2), \dots, (v_{k-1, v_k), then d[v_k] = δ(s, v_k) regardless of other relaxations.

---

## 3. Dijkstra's Algorithm (Non-Negative Weights: w(u, v) ≥ 0)

Prof. Devadas presents Dijkstra's algorithm as a **generalization of Breadth-First Search (BFS)** where unit-cost edges are replaced by arbitrary non-negative weights, and the FIFO queue is replaced by a priority queue:

```text
Dijkstra(G, w, s):
1. Initialize-Single-Source(G, s)
2. S = empty_set                // Set of vertices whose final shortest paths are determined
3. Q = V[G]                      // Priority queue keyed by d[] values
4. while Q is not empty:
5.     u = Extract-Min(Q)
6.     S = S union {u}
7.     for each vertex v in Adj[u]:
8.         Relax(u, v, w)
```

---

## 4. Correctness Proof (Loop Invariant)

**Theorem**: At the start of each iteration of the while loop, d[u] = δ(s, u) for every vertex u in S.

### Proof by Contradiction:
Suppose u is the first vertex added to S for which d[u] ≠ δ(s, u).
Since d[s] = 0 = δ(s, s), u ≠ s, so S ≠ \emptyset just before adding u.
Let p be a true shortest path from s to u.
Since s in S and u \notin S, path p must at some point leave S.
Let (x, y) be the first edge on p such that x in S and y \notin S (potentially y = u).

1. Because x in S, and u was the *first* error, x was correctly finalized: d[x] = δ(s, x).
2. When x was added to S, edge (x, y) was relaxed, so by the Convergence Property:
   
```
d[y] = δ(s, y)
```

3. Because edge weights are **non-negative** (w ≥ 0), subpath distances are non-decreasing along p:
   
```
δ(s, y) ≤ δ(s, u)
```

4. By the Upper-Bound Property, d[u] ≥ δ(s, u), so:
   
```
d[y] = δ(s, y) ≤ δ(s, u) ≤ d[u]
```

5. But the algorithm chose u from Q instead of y, meaning d[u] ≤ d[y].
6. Therefore:
   
```
d[y] = δ(s, y) = δ(s, u) = d[u]
```

Contradicting our assumption that d[u] ≠ δ(s, u)!
Hence, d[u] = δ(s, u) when u is added to S.

---

## 5. Summary of Data Structure Running Times

| Priority Queue Implementation | `Extract-Min` Time | `Decrease-Key` Time | Total Dijkstra Runtime | Optimal For |
| :--- | :--- | :--- | :--- | :--- |
| **Array (Unsorted)** | O(V) | O(1) | O(V² + E) = O(V²) | Dense graphs (E ≈ V²) |
| **Binary Min-Heap** | O(log V) | O(log V) | O((V + E) log V) | Sparse graphs (E ≪ V²) |
| **Fibonacci Heap** | O(log V) (amortized) | O(1) (amortized) | O(V log V + E) | Asymptotically fastest |
