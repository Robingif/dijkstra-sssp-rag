# GeeksforGeeks: Dijkstra's Algorithm for Adjacency List (Min-Heap / Priority Queue)

**Source**: GeeksforGeeks (https://www.geeksforgeeks.org/dijkstras-algorithm-for-adjacency-list-representation-greedy-algo-8/)  
**Topic**: Optimized Dijkstra using Priority Queues on Sparse Graphs  
**Complexity**: Time: O((V + E) log V), Space: O(V + E)  
**Applicability**: Sparse Graphs (E ≪ V²), Non-negative weights  

---

## 1. Why Use Min-Heap / Priority Queue?

In the standard O(V²) implementation, finding the vertex with the minimum distance takes O(V) linear scan time at each iteration.
For sparse graphs where E ≪ V², this linear scan dominates runtime.
By organizing tentative distances in a **Min-Heap (Priority Queue)**:
- Finding and extracting the minimum distance vertex (`extract-min`) takes O(log V) instead of O(V).
- Relaxing an edge requires a `decrease-key` operation in the heap, taking O(log V).
- Each vertex is extracted once (V log V), and each edge is relaxed at most once (E log V).
- Total Time Complexity reduces to O((V + E) log V).

---

## 2. Priority Queue Strategies: Decrease-Key vs Lazy Deletion

Standard binary min-heaps in textbook algorithms support an explicit `decrease-key` operation in O(log V) if heap indices are tracked with an auxiliary map.
In standard programming languages (Python `heapq`, C++ `std::priority_queue`, Java `PriorityQueue`):
- Explicit `decrease-key` is not natively supported in constant time without node handles.
- **The "Lazy Deletion" approach** is standard in competitive programming and production:
  - Whenever a shorter distance to vertex `v` is discovered, simply push a new pair `(new_dist, v)` into the priority queue.
  - When popping `(dist, u)` from the heap, if `dist > dist[u]`, it represents an outdated, superseded entry; simply `continue` (skip it).
  - This preserves correctness and achieves the exact same O((V + E) log V) time bound, using at most E entries in the heap.

---

## 3. Algorithm Specification

```text
Algorithm Dijkstra_MinHeap(Graph G, Source s):
1. Create distance array dist[] of size V, set dist[s] = 0, dist[v] = infinity for all v != s.
2. Initialize Min-Priority-Queue PQ.
3. Insert (0, s) into PQ.
4. While PQ is not empty:
     a. (d, u) = PQ.pop()
     b. If d > dist[u]: continue   // Skip stale entries
     c. For each neighbor (v, weight) in G.adj[u]:
          If dist[u] + weight < dist[v]:
             dist[v] = dist[u] + weight
             parent[v] = u
             PQ.push((dist[v], v))
5. Return dist[], parent[]
```

---

## 4. Production Python Implementation using `heapq`

```python
import heapq
from typing import List, Tuple, Dict

def dijkstra_min_heap(V: int, adj: List[List[Tuple[int, int]]], src: int) -> Tuple[List[float], List[int]]:
    """
    Computes single-source shortest paths using an adjacency list and min-heap.
    
    Args:
        V: Number of vertices (0 to V-1)
        adj: Adjacency list where adj[u] contains (v, weight) tuples
        src: Starting vertex
        
    Returns:
        (dist, parent): Shortest distances and path predecessors
    """
    dist = [float('inf')] * V
    parent = [-1] * V
    dist[src] = 0.0
    
    # Priority queue stores tuples of (distance, vertex)
    pq = [(0.0, src)]
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        # Lazy deletion: skip if we've already found a shorter path to u
        if current_dist > dist[u]:
            continue
            
        for v, weight in adj[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
                
    return dist, parent
```

---

## 5. Detailed Asymptotic Analysis

| Operation | Total Calls | Cost per Call (Binary Heap) | Total Cost |
| :--- | :--- | :--- | :--- |
| `heap_insert` (initial) | 1 | O(log V) | O(log V) |
| `extract_min` | V | O(log V) | O(V log V) |
| `relax_edge` / `heap_push` | E | O(log V) | O(E log V) |
| **Total Time** | | | **O((V + E) log V)** |

- **Dense Graphs (E ≈ V²)**: O(V² log V) — slightly slower than adjacency matrix O(V²) due to heap overhead.
- **Sparse Graphs (E = O(V))**: O(V log V) — vastly superior to O(V²). For V = 100,000 and E = 200,000, O(V log V) ≈ 3.3 × 10^6 ops vs O(V²) ≈ 10^{10 ops!
