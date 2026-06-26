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
// import java.util.*;
static int bfsGrid(char[][] g, int si, int sj, int ti, int tj) {
    int m = g.length, n = g[0].length;
    int[][] dist = new int[m][n];
    for (int[] row : dist) Arrays.fill(row, -1);
    ArrayDeque<int[]> q = new ArrayDeque<>();
    q.offer(new int[] {si, sj});
    dist[si][sj] = 0;
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    while (!q.isEmpty()) {
        int[] cur = q.poll();
        int i = cur[0], j = cur[1];
        if (i == ti && j == tj) return dist[i][j];
        for (int[] d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && g[ni][nj] != '#'
                    && dist[ni][nj] == -1) {
                dist[ni][nj] = dist[i][j] + 1;
                q.offer(new int[] {ni, nj});
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
// import java.util.*;
static int multiBfs(char[][] g, List<int[]> sources) {
    int m = g.length, n = g[0].length;
    int[][] dist = new int[m][n];
    for (int[] row : dist) Arrays.fill(row, -1);
    ArrayDeque<int[]> q = new ArrayDeque<>();
    for (int[] s : sources) {
        dist[s[0]][s[1]] = 0;
        q.offer(s);
    }
    int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    int best = 0;
    while (!q.isEmpty()) {
        int[] cur = q.poll();
        int i = cur[0], j = cur[1];
        for (int[] d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni >= 0 && ni < m && nj >= 0 && nj < n && g[ni][nj] != '#'
                    && dist[ni][nj] == -1) {
                dist[ni][nj] = dist[i][j] + 1;
                best = Math.max(best, dist[ni][nj]);
                q.offer(new int[] {ni, nj});
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
// import java.util.*;
static int bfsMask(int n, List<List<Integer>> g, int start) {
    int full = (1 << n) - 1;
    boolean[][] vis = new boolean[n][1 << n];
    ArrayDeque<int[]> q = new ArrayDeque<>();
    q.offer(new int[] {start, 1 << start});
    vis[start][1 << start] = true;
    for (int d = 0; !q.isEmpty(); d++) {
        int sz = q.size();
        while (sz-- > 0) {
            int[] cur = q.poll();
            int u = cur[0], mask = cur[1];
            if (mask == full) return d;
            for (int v : g.get(u)) {
                int m2 = mask | (1 << v);
                if (!vis[v][m2]) {
                    vis[v][m2] = true;
                    q.offer(new int[] {v, m2});
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
static List<Integer> topoKahn(int n, List<List<Integer>> g) {
    int[] indeg = new int[n];
    for (int u = 0; u < n; u++) for (int v : g.get(u)) indeg[v]++;
    ArrayDeque<Integer> q = new ArrayDeque<>();
    for (int i = 0; i < n; i++) if (indeg[i] == 0) q.offer(i);
    List<Integer> order = new ArrayList<>();
    while (!q.isEmpty()) {
        int u = q.poll();
        order.add(u);
        for (int v : g.get(u)) if (--indeg[v] == 0) q.offer(v);
    }
    return order.size() == n ? order : List.of();
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
// import java.util.*;
static List<Integer> topoDfs(int n, List<List<Integer>> g) {
    int[] color = new int[n];
    List<Integer> order = new ArrayList<>();
    boolean[] ok = {true};
    for (int i = 0; i < n; i++) {
        if (color[i] == 0) dfs(i, g, color, order, ok);
    }
    if (!ok[0]) return List.of();
    Collections.reverse(order);
    return order;
}

private static void dfs(int u, List<List<Integer>> g, int[] color,
                      List<Integer> order, boolean[] ok) {
    color[u] = 1;
    for (int v : g.get(u)) {
        if (color[v] == 0) dfs(v, g, color, order, ok);
        else if (color[v] == 1) ok[0] = false;
    }
    color[u] = 2;
    order.add(u);
}
```

| ID | Title | Link |
|----|--------|------|
| 802 | Find Eventual Safe States | [Link](https://leetcode.com/problems/find-eventual-safe-states/) |

---

## Dijkstra

Nonnegative weights. Adjacency list: `g[u] = [(v, w), ...]`. Returns distances from source `s`.

```java
// import java.util.*;
static long[] dijkstra(int n, List<List<int[]>> g, int s) {
    long INF = 1L << 60;
    long[] dist = new long[n];
    Arrays.fill(dist, INF);
    dist[s] = 0;
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    pq.offer(new long[] {0, s});
    while (!pq.isEmpty()) {
        long[] cur = pq.poll();
        long d = cur[0];
        int u = (int) cur[1];
        if (d != dist[u]) continue;
        for (int[] e : g.get(u)) {
            int v = e[0], w = e[1];
            if (dist[v] > d + w) {
                dist[v] = d + w;
                pq.offer(new long[] {dist[v], v});
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

**Variant: nodes disappear at given times (3112).** Only relax edge (u,v) if `dist[u] + w < disappear[v]`.

```java
// import java.util.*;
static int[] dijkstraDisappear(int n, List<List<int[]>> g, int[] disappear) {
    int[] dist = new int[n];
    Arrays.fill(dist, -1);
    dist[0] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.offer(new int[] {0, 0});
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int d = cur[0], u = cur[1];
        if (dist[u] != -1 && d > dist[u]) continue;
        for (int[] e : g.get(u)) {
            int v = e[0], w = e[1];
            int nd = d + w;
            if (nd < disappear[v] && (dist[v] == -1 || nd < dist[v])) {
                dist[v] = nd;
                pq.offer(new int[] {nd, v});
            }
        }
    }
    return dist;
}
```

**Variant: grid with earliest-entry times (3341).** Moving costs 1, but you may need to wait to enter the next cell.

```java
// import java.util.*;
static long dijkstraGridOpen(int[][] open) {
    int n = open.length, m = open[0].length;
    long INF = 1L << 60;
    long[][] dist = new long[n][m];
    for (long[] row : dist) Arrays.fill(row, INF);
    dist[0][0] = 0;
    PriorityQueue<long[]> pq = new PriorityQueue<>((a, b) -> Long.compare(a[0], b[0]));
    pq.offer(new long[] {0, 0, 0});
    int[][] dirs = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    while (!pq.isEmpty()) {
        long[] cur = pq.poll();
        long t = cur[0];
        int i = (int) cur[1], j = (int) cur[2];
        if (t != dist[i][j]) continue;
        if (i == n - 1 && j == m - 1) return t;
        for (int[] d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
            long nt = Math.max(t, open[ni][nj]) + 1;
            if (nt < dist[ni][nj]) {
                dist[ni][nj] = nt;
                pq.offer(new long[] {nt, ni, nj});
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
static int[] bfs01(int n, List<List<int[]>> g, int s) {
    int[] dist = new int[n];
    Arrays.fill(dist, 1_000_000_000);
    dist[s] = 0;
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    dq.offerFirst(s);
    while (!dq.isEmpty()) {
        int u = dq.pollFirst();
        for (int[] e : g.get(u)) {
            int v = e[0], w = e[1];
            int nd = dist[u] + w;
            if (nd < dist[v]) {
                dist[v] = nd;
                if (w == 0) dq.offerFirst(v);
                else dq.offerLast(v);
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
// import java.util.*;
static long[] bellmanFordK(int n, int[][] edges, int src, int k) {
    long INF = 1L << 60;
    long[] dist = new long[n];
    Arrays.fill(dist, INF);
    dist[src] = 0;
    for (int i = 0; i <= k; i++) {
        long[] ndist = dist.clone();
        for (int[] e : edges) {
            int u = e[0], v = e[1], w = e[2];
            if (dist[u] != INF && dist[u] + w < ndist[v]) ndist[v] = dist[u] + w;
        }
        dist = ndist;
    }
    return dist;
}
```

| ID | Title | Link |
|----|--------|------|
| 787 | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) |

---

## Tarjan (SCC / bridges)

SCC: same low-link = same component. Bridges: edge (u,v) is bridge iff `low[v] > tin[u]`.

```java
// import java.util.*;
static class Tarjan {
    int n, timer = 0, ncomp = 0;
    List<List<Integer>> g;
    int[] tin, low, comp;
    List<Integer> st = new ArrayList<>();
    boolean[] in;

    Tarjan(int n) {
        this.n = n;
        g = new ArrayList<>();
        for (int i = 0; i < n; i++) g.add(new ArrayList<>());
        tin = new int[n];
        low = new int[n];
        comp = new int[n];
        in = new boolean[n];
        Arrays.fill(tin, -1);
        Arrays.fill(comp, -1);
    }

    void add(int u, int v) { g.get(u).add(v); }

    void dfs(int u) {
        tin[u] = low[u] = timer++;
        st.add(u);
        in[u] = true;
        for (int v : g.get(u)) {
            if (tin[v] == -1) {
                dfs(v);
                low[u] = Math.min(low[u], low[v]);
            } else if (in[v]) {
                low[u] = Math.min(low[u], tin[v]);
            }
        }
        if (low[u] == tin[u]) {
            while (true > 0) {
                int v = st.remove(st.size() - 1);
                in[v] = false;
                comp[v] = ncomp;
                if (v == u) break;
            }
            ncomp++;
        }
    }

    int run() {
        for (int i = 0; i < n; i++) if (tin[i] == -1) dfs(i);
        return ncomp;
    }
}
```

```java
// import java.util.*;
static List<int[]> bridges(int n, List<List<Integer>> g) {
    int timer = 0;
    int[] tin = new int[n], low = new int[n];
    Arrays.fill(tin, -1);
    List<int[]> out = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        if (tin[i] == -1) bridgeDfs(i, -1, g, tin, low, new int[] {0}, out);
    }
    return out;
}

private static void bridgeDfs(int u, int p, List<List<Integer>> g,
        int[] tin, int[] low, int[] timer, List<int[]> out) {
    tin[u] = low[u] = timer[0]++;
    for (int v : g.get(u)) {
        if (tin[v] == -1) {
            bridgeDfs(v, u, g, tin, low, timer, out);
            low[u] = Math.min(low[u], low[v]);
            if (low[v] > tin[u]) out.add(new int[] {u, v});
        } else if (v != p) {
            low[u] = Math.min(low[u], tin[v]);
        }
    }
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
| 1202 | Smallest String With Swaps | [Link](https://leetcode.com/problems/smallest-string-with-swaps/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2026-03-09-medium-1202-smallest-string-with-swaps/) |
| 1319 | Number of Operations to Make Network Connected | [Link](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2026-03-10-medium-1319-number-of-operations-to-make-network-connected/) |
| 1584 | Min Cost to Connect All Points | [Link](https://leetcode.com/problems/min-cost-to-connect-all-points/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2026-03-08-medium-1584-min-cost-to-connect-all-points/) |
| 261 | Graph Valid Tree | [Link](https://leetcode.com/problems/graph-valid-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2026-04-01-medium-261-graph-valid-tree/) |

---

## More templates

- **Data structures (DSU, segment tree, etc.):** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
- **Binary search, rotated array, 2D:** [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}
