# GeeksforGeeks: Why Dijkstra's Algorithm Fails on Negative Weights and Negative Cycles

**Source**: GeeksforGeeks (https://www.geeksforgeeks.org/why-does-dijkstras-algorithm-fail-on-negative-weights/)  
**Topic**: Algorithm Correctness, Invariant Breakdown, and Counterexamples  
**Key Takeaway**: Dijkstra's algorithm fundamentally relies on the greedy assumption that adding an edge to a path can never decrease its total weight. Negative edges violate this assumption.

---

## 1. The Core Greedy Assumption

Dijkstra's algorithm is built on the following invariant:
> **The Greedy Invariant**: Once a vertex u is extracted from the priority queue / marked as included in the Shortest Path Tree (`sptSet[u] = True`), its tentative distance `dist[u]` is strictly optimal and will never decrease in the future.

This invariant is proven by induction under the strict premise that **all edge weights w(u, v) ≥ 0**.
Because all edge weights are non-negative, any alternative unexamined path from source to u that passes through other unprocessed vertices must accumulate additional non-negative costs:

```
Cost(Path) = dist[v] + sum w(e) ≥ dist[u]
```

Since dist[v] ≥ dist[u] at the moment u is selected, no longer path can ever be strictly shorter.

---

## 2. How Negative Weights Break the Invariant

When negative edge weights are present (w(u, v) < 0):
- Adding an edge can **decrease** the total path length.
- A path through an unvisited vertex with higher initial distance can suddenly become shorter if it traverses a large negative edge.
- However, because Dijkstra's algorithm **never re-evaluates or re-inserts a finalized vertex**, it will output suboptimal distances or even enter an infinite cycle if negative cycles exist!

---

## 3. Concrete 3-Node Counterexample

Consider a directed graph with 3 vertices: `A (Source)`, `B`, and `C`:
- Edge (A, B) with weight +5
- Edge (A, C) with weight +2
- Edge (B, C) with weight -6

```text
       (A)
      /   \
  +5 /     \ +2
    v       v
   (B)----->(C)
       -6
```

### Trace with Dijkstra's Algorithm:
1. Initialize: `dist[A] = 0`, `dist[B] = inf`, `dist[C] = inf`.
2. Extract A (`dist[A] = 0`):
   - Relax (A, B) \implies dist[B] = 0 + 5 = 5.
   - Relax (A, C) \implies dist[C] = 0 + 2 = 2.
   - Priority Queue: `[(2, C), (5, B)]`. Finalize A.
3. Extract minimum from PQ: C (`dist[C] = 2`):
   - Finalize C (marked visited).
   - C has no outgoing edges.
4. Extract B (`dist[B] = 5`):
   - Finalize B.
   - Examine outgoing edge (B, C) with weight -6:
     
```
dist[B] + (-6) = 5 - 6 = -1
```

   - Since C has **already been finalized**, standard Dijkstra either:
     a) Ignores C because C is in `sptSet`, leaving `dist[C] = 2` (**INCORRECT**: true shortest path is A → B → C = -1).
     b) Or if un-finalized, introduces non-terminating cycles on negative loops.

---

## 4. Negative Cycles

A **negative weight cycle** is a cycle where the sum of edge weights is strictly negative:

```
sum_{e \in C w(e) < 0
```

- If a graph contains a negative cycle reachable from the source, shortest paths to all vertices reachable from that cycle are **undefined (-∞)**, because one can traverse the cycle infinitely many times to decrease the path cost arbitrarily.
- Dijkstra's algorithm cannot detect negative cycles and will either give incorrect answers or loop infinitely.

---

## 5. What to Use Instead: Algorithm Comparison

| Scenario | Recommended Algorithm | Time Complexity | Negative Edges? | Negative Cycle Detection? |
| :--- | :--- | :--- | :--- | :--- |
| **All weights ≥ 0 (Sparse)** | **Dijkstra (Min-Heap)** | O((V + E) log V) | ❌ Fails | ❌ Cannot detect |
| **All weights ≥ 0 (Dense)** | **Dijkstra (Matrix)** | O(V²) | ❌ Fails | ❌ Cannot detect |
| **General weights (Directed/DAG)** | **Topological Sort Relaxation** | O(V + E) | ✅ Works | ✅ Works (DAG has no cycles) |
| **General weights (Arbitrary graph)** | **Bellman-Ford Algorithm** | O(V · E) | ✅ Works | ✅ Detects negative cycles |
| **All-Pairs Shortest Paths** | **Floyd-Warshall** | O(V³) | ✅ Works (No neg cycles) | ✅ Detects on diagonal d[i][i] < 0 |
| **All-Pairs Sparse with Negative Edges** | **Johnson's Algorithm** | O(V² log V + VE) | ✅ Uses Bellman-Ford reweighting | ✅ Detects negative cycles |
