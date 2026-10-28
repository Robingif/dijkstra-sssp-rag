# MIT 6.006 Fall 2011: Lecture 16 — Shortest Paths II: Dijkstra's Algorithm
**Course**: MIT 6.006 Introduction to Algorithms / MIT 6.046J Design and Analysis of Algorithms  
**Instructors**: Prof. Erik Demaine and Prof. Srinivas Devadas  
**Department**: Electrical Engineering and Computer Science, Massachusetts Institute of Technology  
**Source**: MIT OpenCourseWare (https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/) & Lecture 16 Video (https://www.youtube.com/playlist?list=PLUl4u3cNGP6317WaSNfmCvGym2ucw3oGp)  
**Assigned Readings**: CLRS (Cormen, Leiserson, Rivest, Stein), Sections 24.2 - 24.3  

## 1. Problem Formulation: Single-Source Shortest Paths (SSSP)
In MIT 6.006 Lecture 16, Prof. Erik Demaine and Prof. Srinivas Devadas define the Single-Source Shortest Paths (SSSP) problem on a weighted directed or undirected graph G = (V, E) with weight function w: E -> Real Numbers.

- **Objective**: Given a designated source vertex s in V, compute the minimum weight path from s to every reachable vertex v in V.
- **Shortest Path Weight (delta(s, v))**: The weight of the shortest path from s to v:
  delta(s, v) = min { w(p) : p is a path from s to v }. If v is unreachable from s, delta(s, v) = infinity.
- **Fundamental Assumption for Dijkstra**: For every edge (u, v) in E, we assume non-negative edge weights: w(u, v) >= 0.

## 2. Vertex State Variables
During the execution of Dijkstra's algorithm, each vertex v maintains two key attributes:
1. **Tentative Distance (d[v])**: An upper bound on the true shortest path weight delta(s, v). Initially, d[s] = 0 and d[v] = infinity for all v != s.
2. **Predecessor Pointer (pi[v])**: The predecessor of v along the current candidate shortest path from s. Initially, pi[v] = NIL for all v.

Through iterative edge relaxation, d[v] decreases monotonically until it reaches the true shortest path distance delta(s, v), at which point pi forms a directed Shortest Path Tree (SPT) rooted at s.

## 3. Dijkstra's Algorithm Pseudocode (CLRS / MIT 6.006)
Prof. Erik Demaine presents Dijkstra's algorithm using a Priority Queue Q:

`	ext
DIJKSTRA(G, w, s):
    INITIALIZE-SINGLE-SOURCE(G, s)
    S = empty_set                     // S will store vertices whose final shortest paths are determined
    Q = V[G]                          // Build priority queue Q with all vertices keyed by d[v]
    
    while Q is not empty:
        u = EXTRACT-MIN(Q)            // Greedily extract vertex with smallest tentative distance d[u]
        S = S union {u}               // Finalize vertex u into set S
        
        for each vertex v in Adj[u]:
            RELAX(u, v, w)            // Implicit DECREASE-KEY operation in priority queue Q
`

`	ext
INITIALIZE-SINGLE-SOURCE(G, s):
    for each vertex v in V[G]:
        d[v] = infinity
        pi[v] = NIL
    d[s] = 0
`

## 4. The Greedy Strategy
Dijkstra's algorithm is fundamentally a **greedy algorithm**. At every iteration of the while loop, it selects the vertex u in V - S with the minimum tentative shortest path estimate d[u] and locks it into the finalized set S.
Because all edge weights are non-negative, any other path from s to u through unvisited vertices must pass through some boundary vertex with distance >= d[u], meaning no shorter path to u can possibly be discovered later.