---
layout: post
title: "Algorithm Templates: BFS"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates bfs graph
permalink: /posts/2025-11-24-leetcode-templates-bfs/
tags: [leetcode, templates, bfs, graph, traversal]
---

{% raw %}
Minimal, copy-paste Java for graph and grid BFS, multi-source BFS, shortest path, and level-order traversal. See also [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/) for Dijkstra and 0-1 BFS.

## Contents

- [Basic BFS](#basic-bfs)
- [BFS on Grid](#bfs-on-grid)
- [Multi-source BFS](#multi-source-bfs)
- [BFS for Shortest Path](#bfs-for-shortest-path)
- [Level-order Traversal](#level-order-traversal)
- [BFS with State](#bfs-with-state)

## Basic BFS

Breadth-First Search explores nodes level by level using a queue.

```java
// import java.util.*;
// BFS on graph (adjacency list)
static void bfs(int[][] graph, int start) {
    Queue<Integer> q = new LinkedList<>();
    boolean[]visited(graph.size(), false);

    q.offer(start);
    visited[start] = true;

    while (!q.isEmpty()) {
        int node = q.get(0);
        q.poll();

        // Process node
        cout << node << " ";

        // Explore neighbors
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.offer(neighbor);
            }
        }
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 841 | Keys and Rooms | [Link](https://leetcode.com/problems/keys-and-rooms/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/12/medium-841-keys-and-rooms/) |

## BFS on Grid

BFS for 2D grid problems (4-directional or 8-directional).

```java
// import java.util.*;
// BFS on 2D grid (4-directional)
static int bfsGrid(char[][]& grid, int[] start, int[] target) {
    int m = grid.length, n = grid[0].length;
    queue<int[]> q;
    int[][] dist(m, int[](n, -1));
    List<int[]> dirs = {{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0}}
    q.offer(start);
    dist[start[0]][start[1]] = 0;

    while (!q.isEmpty()) {
        auto [x, y] = q.get(0);
        q.poll();

        if (new int[] {x, y} == target) {
            return dist[x][y];
        }

        for (var e : dirs.entrySet()) {
            int nx = x + dx, ny = y + dy;
            if (nx >= 0 && nx < m && ny >= 0 && ny < n &&
                grid[nx][ny] != '#' && dist[nx][ny] == -1) {
                dist[nx][ny] = dist[x][y] + 1;
                q.offer(new int[] {nx, ny});
            }
        }
    }

    return -1;
}

// Count connected components (Number of Islands)
static int numIslands(char[][]& grid) {
    int m = grid.length, n = grid[0].length;
    int count = 0;
    List<int[]> dirs = {{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0}}
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] == '1') {
                count++;
                queue<int[]> q;
                q.offer(new int[] {i, j});
                grid[i][j] = '0';

                while (!q.isEmpty()) {
                    auto [x, y] = q.get(0);
                    q.poll();

                    for (var e : dirs.entrySet()) {
                        int nx = x + dx, ny = y + dy;
                        if (nx >= 0 && nx < m && ny >= 0 && ny < n &&
                            grid[nx][ny] == '1') {
                            grid[nx][ny] = '0';
                            q.offer(new int[] {nx, ny});
                        }
                    }
                }
            }
        }
    }

    return count;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 200 | Number of Islands | [Link](https://leetcode.com/problems/number-of-islands/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-20-medium-200-number-of-islands/) |
| 695 | Max Area of Island | [Link](https://leetcode.com/problems/max-area-of-island/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/20/medium-695-max-area-of-island/) |

## Multi-source BFS

Start BFS from multiple sources simultaneously.

```java
// import java.util.*;
// Multi-source BFS (e.g., 01 Matrix)
int[][] updateMatrix(int[][] mat) {
    int m = mat.length, n = mat[0].length;
    queue<int[]> q;
    int[][] dist(m, int[](n, -1));
    List<int[]> dirs = {{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0}}
    // Add all zeros as starting points
    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (mat[i][j] == 0) {
                q.offer(new int[] {i, j});
                dist[i][j] = 0;
            }
        }
    }

    while (!q.isEmpty()) {
        auto [x, y] = q.get(0);
        q.poll();

        for (var e : dirs.entrySet()) {
            int nx = x + dx, ny = y + dy;
            if (nx >= 0 && nx < m && ny >= 0 && ny < n && dist[nx][ny] == -1) {
                dist[nx][ny] = dist[x][y] + 1;
                q.offer(new int[] {nx, ny});
            }
        }
    }

    return dist;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 286 | Walls and Gates | [Link](https://leetcode.com/problems/walls-and-gates/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-14-medium-286-walls-and-gates/) |
| 542 | 01 Matrix | [Link](https://leetcode.com/problems/01-matrix/) | - |
| 317 | Shortest Distance from All Buildings | [Link](https://leetcode.com/problems/shortest-distance-from-all-buildings/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/09/24/hard-317-shortest-distance-from-all-buildings/) |
| 994 | Rotting Oranges | [Link](https://leetcode.com/problems/rotting-oranges/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-13-medium-994-rotting-oranges/) |

## BFS for Shortest Path

BFS finds shortest path in unweighted graphs.

```java
// import java.util.*;
// Shortest path in unweighted graph
static int shortestPath(int[][] graph, int start, int target) {
    Queue<Integer> q = new LinkedList<>();
    int[]dist(graph.size(), -1);

    q.offer(start);
    dist[start] = 0;

    while (!q.isEmpty()) {
        int node = q.get(0);
        q.poll();

        if (node == target) {
            return dist[node];
        }

        for (int neighbor : graph[node]) {
            if (dist[neighbor] == -1) {
                dist[neighbor] = dist[node] + 1;
                q.offer(neighbor);
            }
        }
    }

    return -1;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 1091 | Shortest Path in Binary Matrix | [Link](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/11/medium-1091-shortest-path-in-binary-matrix/) |
| 127 | Word Ladder | [Link](https://leetcode.com/problems/word-ladder/) | - |
| 433 | Minimum Genetic Mutation | [Link](https://leetcode.com/problems/minimum-genetic-mutation/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/15/medium-433-minimum-genetic-mutation/) |
| 1197 | Minimum Knight Moves | [Link](https://leetcode.com/problems/minimum-knight-moves/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/19/medium-1197-minimum-knight-moves/) |

## Level-order Traversal

BFS for tree level-order traversal.

```java
// import java.util.*;
// Binary Tree Level Order Traversal
int[][] levelOrder(TreeNode root) {
    List<int[]> result = new ArrayList<>();
    if (!root) return result;

    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);

    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>();

        for (int i = 0; i < size; ++i) {
            TreeNode node = q.get(0);
            q.poll();
            level.add(node.val);

            if (node.left) q.offer(node.left);
            if (node.right) q.offer(node.right);
        }

        result.add(level);
    }

    return result;
}

// Zigzag Level Order Traversal
int[][] zigzagLevelOrder(TreeNode root) {
    List<int[]> result = new ArrayList<>();
    if (!root) return result;

    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);
    boolean leftToRight = true;

    while (!q.isEmpty()) {
        int size = q.size();
        int[] level = new int[size];

        for (int i = 0; i < size; ++i) {
            TreeNode node = q.get(0);
            q.poll();

            int index = leftToRight ? i : size - 1 - i;
            level[index] = node.val;

            if (node.left) q.offer(node.left);
            if (node.right) q.offer(node.right);
        }

        result.add(level);
        leftToRight = !leftToRight;
    }

    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 102 | Binary Tree Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/07/medium-102-binary-tree-level-order-traversal/) |
| 103 | Binary Tree Zigzag Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/06/medium-103-binary-tree-zigzag-level-order-traversal/) |
| 314 | Binary Tree Vertical Order Traversal | [Link](https://leetcode.com/problems/binary-tree-vertical-order-traversal/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/20/medium-314-binary-tree-vertical-order-traversal/) |
| 429 | N-ary Tree Level Order Traversal | [Link](https://leetcode.com/problems/n-ary-tree-level-order-traversal/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/07/medium-429-n-ary-tree-level-order-traversal/) |
| 993 | Cousins in Binary Tree | [Link](https://leetcode.com/problems/cousins-in-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/07/easy-993-cousins-in-binary-tree/) |
| 863 | All Nodes Distance K in Binary Tree | [Link](https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-25-medium-863-all-nodes-distance-k-in-binary-tree/) |

## BFS with State

BFS when state includes more than just position.

```java
// import java.util.*;
// BFS with state (e.g., Shortest Path with Obstacle Elimination)
static int shortestPath(int[][] grid, int k) {
    int m = grid.length, n = grid[0].length;
    vector<boolean[][]> visited(m, boolean[][](n, boolean[](k + 1, false)));
    queue<int[]> q; // {x, y, obstacles_eliminated, steps}

    q.offer({0, 0, 0, 0});
    visited[0][0][0] = true;
    List<int[]> dirs = {{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0}}
    while (!q.isEmpty()) {
        var state = q.get(0);
        q.poll();
        int x = state[0], y = state[1], obstacles = state[2], steps = state[3];

        if (x == m - 1 && y == n - 1) {
            return steps;
        }

        for (var e : dirs.entrySet()) {
            int nx = x + dx, ny = y + dy;
            if (nx >= 0 && nx < m && ny >= 0 && ny < n) {
                int newObstacles = obstacles + grid[nx][ny];
                if (newObstacles <= k && !visited[nx][ny][newObstacles]) {
                    visited[nx][ny][newObstacles] = true;
                    q.offer({nx, ny, newObstacles, steps + 1});
                }
            }
        }
    }

    return -1;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 1293 | Shortest Path in a Grid with Obstacles Elimination | [Link](https://leetcode.com/problems/shortest-path-in-a-grid-with-obstacles-elimination/) | - |
| 847 | Shortest Path Visiting All Nodes | [Link](https://leetcode.com/problems/shortest-path-visiting-all-nodes/) | - |

## More templates

- **Graph (Dijkstra, 0-1 BFS, topo):** [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/)
- **Data structures, Search:** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/), [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}

