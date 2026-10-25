# GeeksforGeeks: Dijkstra's Algorithm using `std::set` in C++ STL

**Source**: GeeksforGeeks (https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-set-in-stl/)  
**Topic**: Implementing Dijkstra with Self-Balancing Binary Search Trees  
**Complexity**: Time: O((V + E) log V), Space: O(V)  

---

## 1. Motivation: Why `std::set` over `std::priority_queue`?

In C++ STL, `std::priority_queue` does not support the `decrease-key` operation.
As a result, when using `priority_queue`, we must push redundant pairs `(new_dist, v)` into the queue and rely on lazy deletion, causing the queue size to grow up to O(E).

In contrast, **`std::set` in C++** is implemented as a Red-Black Tree (Self-Balancing BST):
- It stores unique elements in sorted order.
- It supports logarithmic lookup, insertion, and **deletion (`set::erase`)** in O(log N).
- This enables an explicit `decrease-key` emulation:
  1. If vertex `v` has already been inserted with distance `dist[v]`, find and **erase** `(dist[v], v)` from the set.
  2. Insert the updated pair `(new_dist, v)` into the set.
- Consequently, the set contains at most **V elements at any given time**, keeping space bounded by O(V) rather than O(E).

---

## 2. Complete C++ Implementation using `std::set`

```cpp
#include <iostream>
#include <vector>
#include <set>

using namespace std;

const int INF = 1e9;

// Structure to represent an edge (target_node, weight)
typedef pair<int, int> pii;

void dijkstraSet(int V, const vector<vector<pii>>& adj, int src) {
    // Distance vector initialized to infinity
    vector<int> dist(V, INF);
    dist[src] = 0;

    // Set stores pairs of (distance, vertex)
    set<pair<int, int>> st;
    st.insert({0, src});

    while (!st.empty()) {
        // Extract the minimum distance vertex
        auto top = *(st.begin());
        st.erase(st.begin());

        int d = top.first;
        int u = top.second;

        // Traverse all adjacent edges of vertex u
        for (const auto& edge : adj[u]) {
            int v = edge.first;
            int weight = edge.second;

            // Relaxation condition
            if (dist[u] + weight < dist[v]) {
                // If vertex v is already present in the set with an older distance, erase it
                if (dist[v] != INF) {
                    st.erase(st.find({dist[v], v}));
                }

                // Update distance and insert new pair
                dist[v] = dist[u] + weight;
                st.insert({dist[v], v});
            }
        }
    }

    // Print calculated shortest distances
    cout << "Vertex\tDistance from Source (" << src << ")\n";
    for (int i = 0; i < V; ++i) {
        cout << i << "\t" << (dist[i] == INF ? -1 : dist[i]) << "\n";
    }
}
```

---

## 3. Comparison: `std::set` vs `std::priority_queue`

| Feature | `std::set` | `std::priority_queue` |
| :--- | :--- | :--- |
| **Underlying Data Structure** | Red-Black Tree (Self-balancing BST) | Binary Heap (Contiguous Array / Vector) |
| **Max Container Size** | V | E (due to duplicates) |
| **Cache Locality** | Lower (node-based pointer chasing) | Higher (flat array representation) |
| **Constant Factors** | Higher constant multiplier | Lower constant multiplier |
| **Typical Execution Speed** | Slightly slower in practice | Often faster despite duplicate entries |
