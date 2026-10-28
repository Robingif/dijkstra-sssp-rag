# MIT 6.006 Fall 2011: Edge Relaxation & Mathematical Invariant Proofs
**Course**: MIT 6.006 / 6.046J (Prof. Erik Demaine & Prof. Srinivas Devadas)  
**Readings**: CLRS Chapter 24 (Sections 24.2 - 24.3)  
**Source**: MIT OpenCourseWare Lecture 16  

## 1. The Edge Relaxation Subroutine
In MIT 6.006, Prof. Srinivas Devadas and Prof. Erik Demaine explain that the fundamental atomic operation in shortest path algorithms is **Edge Relaxation**:

`	ext
RELAX(u, v, w):
    if d[v] > d[u] + w(u, v):
        d[v] = d[u] + w(u, v)
        pi[v] = u
`

### Intuition:
Relaxing an edge (u, v) tests whether going through vertex u to reach vertex v improves the current shortest path estimate d[v]. If going through u yields a strictly shorter route (d[u] + w(u, v) < d[v]), we update d[v] and record u as the predecessor pi[v].

## 2. The Safety Lemma: Upper-Bound Invariant
**Lemma**: The relaxation algorithm maintains the invariant that d[v] >= delta(s, v) for all v in V at all times during execution. Moreover, once d[v] reaches delta(s, v), it never changes.

### Mathematical Proof by Induction (Prof. Erik Demaine):
1. **Base Case**: Immediately after initialization, d[s] = 0 = delta(s, s) (assuming no negative cycles), and d[v] = infinity >= delta(s, v) for all v != s. The invariant holds.
2. **Inductive Step**: Consider the relaxation of an arbitrary edge (u, v) with weight w(u, v). By the inductive hypothesis, d[u] >= delta(s, u).
   By the **Triangle Inequality**, the shortest path from s to v cannot be longer than the shortest path from s to u plus the direct edge from u to v:
   delta(s, v) <= delta(s, u) + w(u, v)
   Since d[u] >= delta(s, u), we have:
   delta(s, v) <= delta(s, u) + w(u, v) <= d[u] + w(u, v)
   Therefore, setting d[v] = d[u] + w(u, v) preserves d[v] >= delta(s, v).
   Relaxation can never reduce d[v] below the true shortest path distance delta(s, v).

## 3. Key Invariant Properties (MIT 6.006 / CLRS Chapter 24)
- **Triangle Inequality**: For any edge (u, v) in E, delta(s, v) <= delta(s, u) + w(u, v).
- **Upper-Bound Property**: d[v] >= delta(s, v) for all v in V, and once d[v] achieves delta(s, v), it never increases or decreases.
- **Convergence Property**: If s -> ... -> u -> v is a shortest path, and d[u] = delta(s, u) at any time prior to relaxing (u, v), then d[v] = delta(s, v) at all times after relaxing (u, v).
- **Predecessor-Subgraph Property**: Once d[v] = delta(s, v) for all v in V, the predecessor subgraph G_pi is a Shortest Path Tree (SPT) rooted at source s.