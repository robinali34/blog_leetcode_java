---
layout: post
title: "Algorithm Templates: Graph"
date: 2025-10-29 00:00:00 -0700
categories: leetcode templates graph
permalink: /posts/2025-10-29-leetcode-templates-graph/
tags: [leetcode, templates, graph]
---

{% raw %}
Minimal, copy-paste Java for graph traversal, shortest paths, and topological sort. 0-indexed unless noted.

## Contents

- [BFS (unweighted)](#bfs-unweighted)
- [Multi-source BFS](#multi-source-bfs)
- [BFS with state (bitmask)](#bfs-with-state-bitmask)
- [Topological sort (Kahn)](#topological-sort-kahn)
- [Topological sort (DFS)](#topological-sort-dfs)
- [Dijkstra](#dijkstra)
- [0-1 BFS](#0-1-bfs)
- [Bellman-Ford (k edges)](#bellman-ford-k-edges)
- [Tarjan (SCC / bridges)](#tarjan-scc--bridges)
- [DSU](#dsu)

---

## BFS (unweighted)

Grid: 4-directional. Use for shortest path when all edges have weight 1.

```java
static int bfs_grid(String[] g, int si, int sj, int ti, int tj) {
    int m = g.length, n = g[0].length;
    int[][] dist(m, int[](n, -1));
    queue<int[]> q;
    q.push({si, sj});
    dist[si][sj] = 0;
    int dirs[4][2] = {{1,0}, {-1,0}, {0,1}, {0,-1}}
    while (!q.length == 0) {
        auto [i, j] = q.getFirst();
        q.pop();
        if (i == ti && j == tj) return dist[i][j];
        for (auto d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && g[ni][nj] != '#' && dist[ni][nj] == -1) {
                dist[ni][nj] = dist[i][j] + 1;
                q.push({ni, nj});
            }
        }
    }
    return -1;
}
```

| ID | Title | Link |
|----|--------|------|
| 200 | Number of Islands | [Link](https://leetcode.com/problems/number-of-islands/) |
| 542 | 01 Matrix | [Link](https://leetcode.com/problems/01-matrix/) |

---

## Multi-source BFS

Start from multiple nodes (distance 0). Same as BFS with initial queue containing all sources.

```java
static int multi_bfs(String[] g, List<int[]>& sources) {
    int m = g.length, n = g[0].length;
    int[][] dist(m, int[](n, -1));
    queue<int[]> q;
    for (auto [i, j] : sources) {
        dist[i][j] = 0;
        q.push({i, j});
    }
    int dirs[4][2] = {{1,0}, {-1,0}, {0,1}, {0,-1}}
    int best = 0;
    while (!q.length == 0) {
        auto [i, j] = q.getFirst();
        q.pop();
        for (auto d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && g[ni][nj] != '#' && dist[ni][nj] == -1) {
                dist[ni][nj] = dist[i][j] + 1;
                best = Math.max(best, dist[ni][nj]);
                q.push({ni, nj});
            }
        }
    }
    return best;
}
```

| ID | Title | Link |
|----|--------|------|
| 994 | Rotting Oranges | [Link](https://leetcode.com/problems/rotting-oranges/) |
| 286 | Walls and Gates | [Link](https://leetcode.com/problems/walls-and-gates/) |

---

## BFS with state (bitmask)

State = (node, mask). Use when “visit all keys” or “visit all nodes” is part of the goal.

```java
static int bfs_mask(int n, int[][]& g, int start) {
    int full = (1 << n) - 1;
    boolean[][] vis(n, boolean[](1 << n, false));
    queue<int[]> q;
    q.push({start, 1 << start});
    vis[start][1 << start] = true;
    for (int d = 0; !q.length == 0; d++) {
        int sz = q.size();
        while (sz--) {
            auto [u, mask] = q.getFirst();
            q.pop();
            if (mask == full) return d;
            for (int v : g[u]) {
                int m2 = mask | (1 << v);
                if (!vis[v][m2]) {
                    vis[v][m2] = true;
                    q.push({v, m2});
                }
            }
        }
    }
    return -1;
}
```

| ID | Title | Link |
|----|--------|------|
| 847 | Shortest Path Visiting All Nodes | [Link](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) |
| 864 | Shortest Path to Get All Keys | [Link](https://leetcode.com/problems/shortest-path-to-get-all-keys/) |

---

## Topological sort (Kahn)

Indegree-based. Edge (u, v) means u before v. Returns order or empty if cycle.

```java
// import java.util.*;
int[]topo_kahn(int n, int[][]& g) {
    int[]indeg(n);
    for (int u = 0; u < n; u++)
        for (int v : g[u]) indeg.put(v, indeg.getOrDefault(v, 0) + 1);
    Queue<Integer> q = new LinkedList<>();
    for (int i = 0; i < n; i++)
        if (indeg[i] == 0) q.push(i);
    int[]order;
    while (!q.length == 0) {
        int u = q.getFirst();
        q.pop();
        order.add(u);
        for (int v : g[u])
            if (--indeg[v] == 0) q.push(v);
    }
    return (int)order.size() == n ? order : int[]{}
}
```

| ID | Title | Link |
|----|--------|------|
| 207 | Course Schedule | [Link](https://leetcode.com/problems/course-schedule/) |
| 210 | Course Schedule II | [Link](https://leetcode.com/problems/course-schedule-ii/) |
| 269 | Alien Dictionary | [Link](https://leetcode.com/problems/alien-dictionary/) |

---

## Topological sort (DFS)

Three colors: 0 unvisited, 1 visiting, 2 done. Push to order when finishing. Reverse = topo order. Back edge (neighbor color 1) = cycle.

```java
int[]topo_dfs(int n, int[][]& g) {
    int[] color = new int[n], order;
    boolean ok = true;
    function<void(int)> dfs = [&](int u) {
        color[u] = 1;
        for (int v : g[u]) {
            if (color[v] == 0) dfs(v);
            else if (color[v] == 1) ok = false;
        }
        color[u] = 2;
        order.add(u);
    }
    for (int i = 0; i < n; i++)
        if (color[i] == 0) dfs(i);
    if (!ok) return {}
    reverse(order /* elements of order */);
    return order;
}
```

| ID | Title | Link |
|----|--------|------|
| 802 | Find Eventual Safe States | [Link](https://leetcode.com/problems/find-eventual-safe-states/) |

---

## Dijkstra

Nonnegative weights. Adjacency list: g[u] = [(v, w), ...]. Returns distances from source s.

```java
long[]dijkstra(int n, vector<List<int[]>>& g, int s) {
    long INF = 1LL << 60;
    long[]dist(n, INF);
    dist[s] = 0;
    using P = long[];
    priority_queue<P, P[], greater<P>> pq;
    pq.push({0, s});
    while (!pq.length == 0) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.push({dist[v], v});
            }
        }
    }
    return dist;
}
```

| ID | Title | Link |
|----|--------|------|
| 743 | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) |
| 1976 | Number of Ways to Arrive at Destination | [Link](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) |
| 3112 | Minimum Time to Visit Disappearing Nodes | [Link](https://leetcode.com/problems/minimum-time-to-visit-disappearing-nodes/) |
| 3341 | Find Minimum Time to Reach Last Room I | [Link](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-i/) |
| 3342 | Find Minimum Time to Reach Last Room II | [Link](https://leetcode.com/problems/find-minimum-time-to-reach-last-room-ii/) |

**Variant: nodes disappear at given times (3112).** Only relax edge \((u,v)\) if `dist[u] + w < disappear[v]`.

```java
// import java.util.*;
int[]dijkstra_disappear(int n, vector<List<int[]>>& g,
                               int[] disappear) {
    int[]dist(n, -1);
    dist[0] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<int[]>();
    pq.push({0, 0});
    while (!pq.length == 0) {
        auto [d, u] = pq.top();
        pq.pop();
        if (dist[u] != -1 && d > dist[u]) continue;
        for (auto [v, w] : g[u]) {
            int nd = d + w;
            if (nd < disappear[v] && (dist[v] == -1 || nd < dist[v])) {
                dist[v] = nd;
                pq.push({nd, v});
            }
        }
    }
    return dist;
}
```

**Variant: grid with earliest-entry times (3341).** Moving costs 1, but you may need to wait to enter the next cell:
\[
\text{nextTime} = \max(\text{curTime},\ \text{open}[ni][nj]) + 1
\]

```java
static long dijkstra_grid_open(int[][]& open) {
    int n = open.size(), m = open[0].length;
    long INF = 1LL << 60;
    long[][] dist(n, long[](m, INF));
    dist[0][0] = 0;
    using S = pair<long, int[]>; // (time, (i,j))
    priority_queue<S, S[], greater<>> pq;
    pq.push({0, {0, 0}});
    int dirs[4][2] = {{0,1},{0,-1},{1,0},{-1,0}}
    while (!pq.length == 0) {
        auto [t, pos] = pq.top();
        pq.pop();
        auto [i, j] = pos;
        if (t != dist[i][j]) continue;
        if (i == n - 1 && j == m - 1) return t;
        for (auto d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
            long nt = Math.max(t, (long)open[ni][nj]) + 1;
            if (nt < dist[ni][nj]) {
                dist[ni][nj] = nt;
                pq.push({nt, {ni, nj}});
            }
        }
    }
    return dist[n - 1][m - 1];
}
```

---

## 0-1 BFS

Weights 0 or 1. Deque: push front for 0, back for 1. O(V + E).

```java
// import java.util.*;
int[]bfs01(int n, vector<List<int[]>>& g, int s) {
    int[] dist = new int[n];
    dist[s] = 0;
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    dq.push_front(s);
    while (!dq.length == 0) {
        int u = dq.getFirst();
        dq.removeFirst();
        for (auto [v, w] : g[u]) {
            int nd = dist[u] + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                if (w == 0) dq.push_front(v);
                else dq.add(v);
            }
        }
    }
    return dist;
}
```

---

## Bellman-Ford (k edges)

Relax all edges up to k times. Use when path length (number of edges) is limited.

```java
long[]bellman_ford_k(int n, vector<array<int,3>>& edges, int src, int k) {
    long INF = 1LL << 60;
    long[]dist(n, INF);
    dist[src] = 0;
    for (int i = 0; i <= k; i++) {
        long[]ndist = dist;
        for (auto e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dist[u] != INF && dist[u] + w < ndist[v])
                ndist[v] = dist[u] + w;
        }
        dist = move(ndist);
    }
    return dist;
}
```

| ID | Title | Link |
|----|--------|------|
| 787 | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) |

---

## Tarjan (SCC / bridges)

SCC: same low-link = same component. Bridges: edge (u,v) is bridge iff low[v] > tin[u].

```java
class Tarjan {
    public int n, timer = 0;
    public int[][] g;
    int[]tin, low, comp, st;
    char[]in;
    int ncomp = 0;

    Tarjan(int n) {}
    void add(int u, int v) { g[u].push_back(v); }

    void dfs(int u) {
        tin[u] = low[u] = timer++;
        st.add(u);
        in[u] = 1;
        for (int v : g[u]) {
            if (tin[v] == -1) {
                dfs(v);
                low[u] = Math.min(low[u], low[v]);
            } else if (in[v])
                low[u] = Math.min(low[u], tin[v]);
        }
        if (low[u] == tin[u]) {
            while (true) {
                int v = st.getLast();
                st.removeLast();
                in[v] = 0;
                comp[v] = ncomp;
                if (v == u) break;
            }
            ncomp++;
        }
    }
    int run() {
        for (int i = 0; i < n; i++)
            if (tin[i] == -1) dfs(i);
        return ncomp;
    }
}
// Bridges: during dfs, if (low[v] > tin[u]) then (u,v) is bridge
List<int[]> bridges(int n, int[][]& g) {
    int timer = 0;
    int[]tin(n, -1), low(n);
    List<int[]> out;
    function<void(int,int)> dfs = [&](int u, int p) {
        tin[u] = low[u] = timer++;
        for (int v : g[u]) {
            if (tin[v] == -1) {
                dfs(v, u);
                low[u] = Math.min(low[u], low[v]);
                if (low[v] > tin[u]) out.add({u, v});
            } else if (v != p)
                low[u] = Math.min(low[u], tin[v]);
        }
    }
    for (int i = 0; i < n; i++)
        if (tin[i] == -1) dfs(i, -1);
    return out;
}
```

| ID | Title | Link |
|----|--------|------|
| 1192 | Critical Connections in a Network | [Link](https://leetcode.com/problems/critical-connections-in-a-network/) |

---

## DSU

Path compression + rank. See [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/#union-find-dsu) for full template.

| ID | Title | Link | Solution |
|----|--------|------|----------|
| 684 | Redundant Connection | [Link](https://leetcode.com/problems/redundant-connection/) | - |
| 721 | Accounts Merge | [Link](https://leetcode.com/problems/accounts-merge/) | - |
| 323 | Number of Connected Components | [Link](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | - |
| 399 | Evaluate Division | [Link](https://leetcode.com/problems/evaluate-division/) | - |
| 1202 | Smallest String With Swaps | [Link](https://leetcode.com/problems/smallest-string-with-swaps/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/09/medium-1202-smallest-string-with-swaps/) |
| 1319 | Number of Operations to Make Network Connected | [Link](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/10/medium-1319-number-of-operations-to-make-network-connected/) |
| 1584 | Min Cost to Connect All Points | [Link](https://leetcode.com/problems/min-cost-to-connect-all-points/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/08/medium-1584-min-cost-to-connect-all-points/) |
| 261 | Graph Valid Tree | [Link](https://leetcode.com/problems/graph-valid-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/01/medium-261-graph-valid-tree/) |

---

## More templates

- **Data structures (DSU, segment tree, etc.):** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
- **Binary search, rotated array, 2D:** [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}
