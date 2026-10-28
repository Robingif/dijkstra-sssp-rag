# MIT 6.006 Fall 2011: Correctness Proof & Why Dijkstra Fails on Negative Weights
**Course**: MIT 6.006 / 6.046J (Prof. Erik Demaine & Prof. Srinivas Devadas)  
**Readings**: CLRS Section 24.3 (Theorem 24.6)  
**Source**: MIT OpenCourseWare Lecture 16  

## 1. Theorem: Correctness of Dijkstra's Algorithm
**Theorem (CLRS 24.6 / MIT 6.006)**: Dijkstra's algorithm, run on a weighted, directed graph G = (V, E) with non-negative weight function w: E -> [0, infinity) and source s, terminates with d[u] = delta(s, u) for all vertices u in V.

### Proof of the Greedy Invariant by Contradiction:
We prove that whenever a vertex u is added to the finalized set S (i.e., extracted from Q via EXTRACT-MIN), d[u] = delta(s, u).
1. Assume for the sake of contradiction that u is the first vertex added to S for which d[u] != delta(s, u).
2. By the Safety Lemma, d[u] >= delta(s, u), so it must be that d[u] > delta(s, u).
3. Consider an actual shortest path p from s to u. Let y be the first vertex on path p that belongs to V - S (the unvisited set), and let x be y's immediate predecessor on p (so x is in S).
4. Since x was added to S before u, and x is not the first incorrect vertex, d[x] = delta(s, x).
5. When x was added to S, edge (x, y) was relaxed, so by the Convergence Property:
   d[y] = delta(s, y)
6. Because edge weights are non-negative (w(e) >= 0), subpath weights are non-decreasing along path p:
   delta(s, y) <= delta(s, u)
7. Since d[u] > delta(s, u), we have:
   d[y] = delta(s, y) <= delta(s, u) < d[u]
   which implies d[y] < d[u].
8. Both u and y were in Q when u was chosen by EXTRACT-MIN. But EXTRACT-MIN chooses the vertex with the minimal d value. Since d[y] < d[u], the algorithm would have chosen y instead of u.
9. This contradiction proves d[u] = delta(s, u) for all vertices u in S.

## 2. Why Dijkstra Fails on Negative Edge Weights
Prof. Erik Demaine emphasizes: **The entire proof of correctness collapses if any edge weight is negative.**

### Where the proof breaks:
In Step 6 of the proof above, we assumed delta(s, y) <= delta(s, u) because the path from y to u cannot have negative weight. If negative edge weights are permitted, a path from y to u could have negative total weight, making delta(s, u) < delta(s, y).
In that scenario:
- A vertex u could be finalized into S with a tentative distance d[u] that is NOT the true shortest path.
- Later, an alternative path through an unvisited node y with negative edge weights could reach u with a lower cost.
- Because Dijkstra NEVER revisits or re-relaxes vertices already in set S, the algorithm terminates with an incorrect distance!

### The 3-Node Counterexample (Prof. Demaine):
- Directed graph with vertices {S, A, B}:
  - Edge (S, A) with weight 3
  - Edge (S, B) with weight 5
  - Edge (B, A) with weight -3
- Step 1: Initialize d[S] = 0, d[A] = inf, d[B] = inf. S_set = empty_set.
- Step 2: Relax from S: d[A] = 3, d[B] = 5.
- Step 3: EXTRACT-MIN picks A (since d[A]=3 < d[B]=5). Vertex A is permanently placed into S!
- Step 4: EXTRACT-MIN picks B (d[B]=5). Relax edge (B, A):
  Candidate path to A through B: d[B] + w(B, A) = 5 + (-3) = 2.
  Notice 2 < 3! The true shortest path from S to A is 2 (path S -> B -> A).
- But Dijkstra has already finalized A and will never update d[A]! Dijkstra incorrectly outputs d[A] = 3 instead of 2.

### What algorithm should be used instead?
When negative edge weights are present, Prof. Demaine instructs students to use the **Bellman-Ford Algorithm** ((V \cdot E)$), which relaxes all edges |V| - 1 times and can detect negative-weight cycles.