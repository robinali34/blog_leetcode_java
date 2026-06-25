---
layout: post
title: "Algorithm Templates: DFS"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates dfs graph
permalink: /posts/2025-11-24-leetcode-templates-dfs/
tags: [leetcode, templates, dfs, graph, traversal]
---

{% raw %}
Minimal, copy-paste Java for graph DFS, grid DFS, tree DFS, memoization, and iterative DFS. See also [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/) and [Backtracking](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-backtracking/).

## Contents

- [Basic DFS](#basic-dfs)
- [DFS on Grid](#dfs-on-grid)
- [DFS on Tree](#dfs-on-tree)
- [DFS with Memoization](#dfs-with-memoization)
- [Iterative DFS](#iterative-dfs)

## Basic DFS

Depth-First Search explores as far as possible before backtracking.

```java
// DFS on graph (adjacency list)
static void dfs(int[][]& graph, int node, boolean[] visited) {
    visited[node] = true;

    // Process node
    cout << node << " ";

    // Explore neighbors
    for (int neighbor : graph[node]) {
        if (!visited[neighbor]) {
            dfs(graph, neighbor, visited);
        }
    }
}

// DFS with return value
static boolean dfs(int[][]& graph, int node, int target, boolean[] visited) {
    if (node == target) return true;
    visited[node] = true;

    for (int neighbor : graph[node]) {
        if (!visited[neighbor] && dfs(graph, neighbor, target, visited)) {
            return true;
        }
    }

    return false;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 841 | Keys and Rooms | [Link](https://leetcode.com/problems/keys-and-rooms/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/12/medium-841-keys-and-rooms/) |

## DFS on Grid

DFS for 2D grid problems (connected components, paths).

```java
// DFS on 2D grid (4-directional)
static void dfsGrid(char[][]& grid, int i, int j) {
    int m = grid.length, n = grid[0].length;

    if (i < 0 || i >= m || j < 0 || j >= n || grid[i][j] != '1') {
        return;
    }

    grid[i][j] = '0'; // Mark as visited

    // Explore 4 directions
    dfsGrid(grid, i + 1, j);
    dfsGrid(grid, i - 1, j);
    dfsGrid(grid, i, j + 1);
    dfsGrid(grid, i, j - 1);
}

// Number of Islands using DFS
static int numIslands(char[][]& grid) {
    int m = grid.length, n = grid[0].length;
    int count = 0;

    for (int i = 0; i < m; ++i) {
        for (int j = 0; j < n; ++j) {
            if (grid[i][j] == '1') {
                count++;
                dfsGrid(grid, i, j);
            }
        }
    }

    return count;
}

// Word Search
static boolean dfsWordSearch(char[][]& board, int i, int j, String word, int idx) {
    if (idx == word.size()) return true;
    if (i < 0 || i >= board.size() || j < 0 || j >= board[0].length) return false;
    if (board[i][j] != word[idx]) return false;

    char temp = board[i][j];
    board[i][j] = '#'; // Mark as visited

    List<int[]> dirs = \{\{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0\}\}
    for (auto& [dx, dy] : dirs) {
        if (dfsWordSearch(board, i + dx, j + dy, word, idx + 1)) {
            return true;
        }
    }

    board[i][j] = temp; // Backtrack
    return false;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 200 | Number of Islands | [Link](https://leetcode.com/problems/number-of-islands/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-20-medium-200-number-of-islands/) |
| 79 | Word Search | [Link](https://leetcode.com/problems/word-search/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/12/medium-79-word-search/) |
| 695 | Max Area of Island | [Link](https://leetcode.com/problems/max-area-of-island/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/20/medium-695-max-area-of-island/) |
| 133 | Clone Graph | [Link](https://leetcode.com/problems/clone-graph/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/20/medium-133-clone-graph/) |
| 417 | Pacific Atlantic Water Flow | [Link](https://leetcode.com/problems/pacific-atlantic-water-flow/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/19/medium-417-pacific-atlantic-water-flow/) |
| 323 | Number of Connected Components | [Link](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/07/medium-323-number-of-connected-components-in-an-undirected-graph/) |
| 547 | Number of Provinces | [Link](https://leetcode.com/problems/number-of-provinces/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-18-medium-547-number-of-provinces/) |

## DFS on Tree

DFS for tree problems (preorder, inorder, postorder).

```java
// Preorder DFS
static void preorder(TreeNode root, int[] result) {
    if (!root) return;
    result.add(root.val);
    preorder(root.left, result);
    preorder(root.right, result);
}

// Inorder DFS
static void inorder(TreeNode root, int[] result) {
    if (!root) return;
    inorder(root.left, result);
    result.add(root.val);
    inorder(root.right, result);
}

// Postorder DFS
static void postorder(TreeNode root, int[] result) {
    if (!root) return;
    postorder(root.left, result);
    postorder(root.right, result);
    result.add(root.val);
}

// Path Sum
static boolean hasPathSum(TreeNode root, int targetSum) {
    if (!root) return false;
    if (!root.left && !root.right) {
        return root.val == targetSum;
    }
    return hasPathSum(root.left, targetSum - root.val) ||
           hasPathSum(root.right, targetSum - root.val);
}

// Sum Root to Leaf Numbers
static int sumNumbers(TreeNode root, int sum) {
    if (!root) return 0;
    sum = sum 10 + root.val;
    if (!root.left && !root.right) return sum;
    return sumNumbers(root.left, sum) + sumNumbers(root.right, sum);
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 100 | Same Tree | [Link](https://leetcode.com/problems/same-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-100-same-tree/) |
| 101 | Symmetric Tree | [Link](https://leetcode.com/problems/symmetric-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-101-symmetric-tree/) |
| 104 | Maximum Depth of Binary Tree | [Link](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-104-maximum-depth-of-binary-tree/) |
| 111 | Minimum Depth of Binary Tree | [Link](https://leetcode.com/problems/minimum-depth-of-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-111-minimum-depth-of-binary-tree/) |
| 112 | Path Sum | [Link](https://leetcode.com/problems/path-sum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-112-path-sum/) |
| 129 | Sum Root to Leaf Numbers | [Link](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-24-medium-129-sum-root-to-leaf-numbers/) |
| 226 | Invert Binary Tree | [Link](https://leetcode.com/problems/invert-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/easy-226-invert-binary-tree/) |
| 236 | Lowest Common Ancestor | [Link](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/19/medium-236-lowest-common-ancestor-of-a-binary-tree/) |
| 437 | Path Sum III | [Link](https://leetcode.com/problems/path-sum-iii/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/10/19/medium-437-path-sum-iii/) |
| 690 | Employee Importance | [Link](https://leetcode.com/problems/employee-importance/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-16-medium-690-employee-importance/) |

## DFS with Memoization

DFS with caching to avoid recomputation.

```java
// DFS with memoization (e.g., Longest Increasing Path)
static int dfsWithMemo(int[][]& matrix, int i, int j,
                int[][]& memo, int prev) {
    int m = matrix.size(), n = matrix[0].length;

    if (i < 0 || i >= m || j < 0 || j >= n || matrix[i][j] <= prev) {
        return 0;
    }

    if (memo[i][j] != -1) {
        return memo[i][j];
    }

    int result = 1;
    List<int[]> dirs = \{\{0,1\}, \{0,-1\}, \{1,0\}, \{-1,0\}\}
    for (auto& [dx, dy] : dirs) {
        result = Math.max(result, 1 + dfsWithMemo(matrix, i + dx, j + dy,
                                              memo, matrix[i][j]));
    }

    memo[i][j] = result;
    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 329 | Longest Increasing Path in a Matrix | [Link](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/18/hard-329-longest-increasing-path-in-a-matrix/) |

## Iterative DFS

DFS using stack instead of recursion.

```java
// import java.util.*;
// Iterative DFS on graph
static void dfsIterative(int[][]& graph, int start) {
    Deque<Integer> st = new ArrayDeque<>();
    boolean[]visited(graph.size(), false);

    st.push(start);

    while (!st.length == 0) {
        int node = st.top();
        st.pop();

        if (visited[node]) continue;
        visited[node] = true;

        // Process node
        cout << node << " ";

        // Push neighbors in reverse order to maintain order
        for (int i = graph[node].size() - 1; i >= 0; --i) {
            if (!visited[graph[node][i]]) {
                st.push(graph[node][i]);
            }
        }
    }
}

// Iterative DFS on tree
int[]preorderIterative(TreeNode root) {
    int[]result;
    if (!root) return result;

    stack<TreeNode> st;
    st.push(root);

    while (!st.length == 0) {
        TreeNode node = st.top();
        st.pop();
        result.add(node.val);

        if (node.right) st.push(node.right);
        if (node.left) st.push(node.left);
    }

    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 144 | Binary Tree Preorder Traversal | [Link](https://leetcode.com/problems/binary-tree-preorder-traversal/) | - |
| 94 | Binary Tree Inorder Traversal | [Link](https://leetcode.com/problems/binary-tree-inorder-traversal/) | - |

## More templates

- **Graph, Backtracking:** [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/), [Backtracking](/blog_leetcode_java/posts/2025-11-24-leetcode-templates-backtracking/)
- **Data structures, Search:** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/), [Search](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}

