# MIT 6.006 Fall 2011: Balls and String Physical Intuition & Shortest Path Variations
**Course**: MIT 6.006 / 6.046J (Prof. Erik Demaine & Prof. Srinivas Devadas)  
**Source**: MIT OpenCourseWare Lecture 16  

## 1. Prof. Erik Demaine's Physical Demonstration: Balls and Strings
In Lecture 16, Prof. Erik Demaine introduces a famous physical model to provide an intuitive understanding of Dijkstra's algorithm:

### The Physical System:
- Imagine every vertex in the graph is a small wooden ball.
- For every directed or undirected edge (u, v) with weight w(u, v), tie a string of length w(u, v) between ball u and ball v.
- Place all balls on a table.
- Now, grasp the source ball s with your fingers and pull it straight up off the table.

### What Happens Physically:
1. As you lift source ball s, balls attached to s by taut strings are lifted off the table one by one.
2. The distance a ball rises corresponds exactly to the shortest path distance delta(s, v)!
3. The sequence in which the balls leave the table corresponds exactly to the order in which Dijkstra's EXTRACT-MIN extracts vertices from the priority queue!
4. The taut strings connecting the lifted balls form the **Shortest Path Tree (SPT)**.

### Why this intuition proves non-negative weights are required:
A string cannot have a negative physical length! A string of negative length would push balls away rather than pull them taut, breaking the physical invariant that strings only pull when taut.

## 2. Shortest Paths in Directed Acyclic Graphs (DAGs)
Prof. Srinivas Devadas highlights that if a graph has no cycles (a Directed Acyclic Graph, or DAG), we can solve the Single-Source Shortest Paths problem even faster than Dijkstra, and even with negative weights:

1. **Step 1**: Topologically sort the vertices of the DAG in O(V + E) time.
2. **Step 2**: Make one single pass over the vertices in topologically sorted order, relaxing all outgoing edges from each vertex:
   `	ext
   DAG-SHORTEST-PATHS(G, w, s):
       topologically sort vertices of G
       INITIALIZE-SINGLE-SOURCE(G, s)
       for each vertex u in topologically sorted order:
           for each vertex v in Adj[u]:
               RELAX(u, v, w)
   `
3. **Total Runtime**: Exactly Theta(V + E) linear time!
4. **Key Insight**: Because there are no cycles in a DAG, there can be no negative cycles. Topological ordering guarantees that when we process vertex u, all possible paths that could reach u have already been relaxed.

## 3. Real-World Applications Discussed in MIT 6.006
Prof. Demaine and Prof. Devadas discuss how SSSP algorithms are foundational to modern infrastructure:
- **Internet Protocol Routing (OSPF & IS-IS)**: Routers running Open Shortest Path First exchange link state advertisements and independently execute Dijkstra's algorithm to compute the shortest routing paths for IP packets.
- **Road Network Routing (Google Maps / GPS)**: Road maps are modeled as large graphs where intersections are vertices and road segments are edges weighted by traversal time. Dijkstra and its heuristic derivative A* compute optimal driving directions.
- **State Space Planning in Robotics**: Robotic motion planning discretizes obstacle-free configuration space into graph nodes, using shortest path graph traversal to compute collision-free trajectories.