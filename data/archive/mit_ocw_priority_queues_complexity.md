# MIT 6.006 Fall 2011: Priority Queue Data Structures & Complexity Analysis
**Course**: MIT 6.006 / 6.046J (Prof. Erik Demaine & Prof. Srinivas Devadas)  
**Readings**: CLRS Section 24.3 & Section 6.5  
**Source**: MIT OpenCourseWare Lecture 16  

## 1. Operation Count Breakdown
In MIT 6.006 Lecture 16, Prof. Erik Demaine analyzes the exact number of priority queue operations performed by Dijkstra's algorithm on a graph G = (V, E):

1. **INSERT operations**: Exactly |V| inserts to populate the priority queue Q during initialization.
2. **EXTRACT-MIN operations**: Exactly |V| extract-min calls, because each vertex is extracted from Q and finalized into set S exactly once.
3. **DECREASE-KEY operations**: At most |E| decrease-key calls, because each directed edge (u, v) in the adjacency list of u is examined and relaxed at most once.

Therefore, the total running time of Dijkstra's algorithm is:
T(V, E) = Theta(V) * T_Insert + Theta(V) * T_ExtractMin + Theta(E) * T_DecreaseKey

## 2. Comparison Across Priority Queue Implementations

### Implementation 1: Unsorted Array / Simple List
- **INSERT**: Theta(1)
- **EXTRACT-MIN**: Theta(V) (linear scan over all remaining vertices in Q to find the minimum distance)
- **DECREASE-KEY**: Theta(1) (direct array indexing d[v] = new_weight)
- **Total Asymptotic Runtime**:
  T(V, E) = Theta(V * 1 + V * V + E * 1) = Theta(V^2 + E) = Theta(V^2)
- **When to use**: Highly dense graphs where |E| is proportional to |V|^2 (E ~ V^2). In this dense limit, an array is simple, has zero pointer overhead, and is asymptotically optimal.

### Implementation 2: Binary Min-Heap (Standard CLRS / MIT 6.006)
- **BUILD-HEAP / INSERT**: Theta(V) total using Floyd's build-heap, or Theta(V log V) via repeated insertions.
- **EXTRACT-MIN**: Theta(log V) (remove root element and bubble down / heapify).
- **DECREASE-KEY**: Theta(log V) (update key and bubble up towards root).
- **Total Asymptotic Runtime**:
  T(V, E) = Theta(V log V + E log V) = Theta((V + E) log V)
- **When to use**: Sparse graphs, road maps, and computer network topologies where |E| << |V|^2 (e.g., planar road networks where E = O(V)). In sparse graphs, Theta((V + E) log V) is vastly faster than Theta(V^2).

### Implementation 3: Fibonacci Heap (Advanced MIT 6.046J)
- **EXTRACT-MIN**: Theta(log V) amortized cost.
- **DECREASE-KEY**: Theta(1) amortized cost.
- **Total Asymptotic Runtime**:
  T(V, E) = Theta(V log V + E)
- **Significance**: Prof. Erik Demaine notes that Fibonacci Heaps achieve theoretical optimality for Dijkstra's algorithm when E is intermediate between V and V^2. While theoretically superior, constant factors in practice make Binary Min-Heaps preferred for most practical software implementations.