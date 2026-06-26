---
layout: post
title: "[Medium] 419. Battleships in a Board"
date: 2025-10-21 17:00:00 -0700
categories: leetcode medium array matrix
permalink: /posts/2025-10-21-medium-419-battleships-in-a-board/
tags: [leetcode, medium, array, matrix, dfs, battleship]
---

# LC 419: Battleships in a Board

**Difficulty:** Medium  
**Category:** Array, Matrix, DFS  
**Companies:** Amazon, Google, Microsoft

## Problem Statement

Given an `m x n` matrix `board` where each cell is either a battleship `'X'` or empty `'.'`, return the number of the battleships on `board`.

Battleships can only be placed horizontally or vertically on `board`. In other words, they can only be made of the shape `1 x k` (1 row, k columns) or `k x 1` (k rows, 1 column), where `k` can be of any size. At least one horizontal or vertical cell separates between two battleships (i.e., there are no adjacent battleships).

### Examples

**Example 1:**
```
Input: board = [["X",".",".","X"],[".",".",".","X"],[".",".",".","X"]]
Output: 2
```

**Example 2:**
```
Input: board = [["."]]
Output: 0
```

### Constraints

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 200`
- `board[i][j]` is either `'.'` or `'X'`

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **Battleship definition**: What is a battleship? (Assumption: Group of 'X' cells - horizontally or vertically adjacent, not diagonally)

2. **Battleship rules**: What are the rules? (Assumption: Battleships don't touch each other - no adjacent battleships horizontally or vertically)

3. **Return value**: What should we return? (Assumption: Integer - count of battleships on the board)

4. **Single cell**: Can a single 'X' be a battleship? (Assumption: Yes - battleship can be 1×1)

5. **Board modification**: Can we modify the board? (Assumption: Typically yes for marking visited, but should clarify)

## Interview Deduction Process (20 minutes)

**Step 1: Brute-Force Approach (5 minutes)**

Use DFS or BFS to find all connected components of 'X' cells. Count each connected component as one battleship. This approach works but requires O(m × n) extra space for visited tracking and O(m × n) time.

**Step 2: Semi-Optimized Approach (7 minutes)**

Use DFS with in-place marking: mark visited cells by changing 'X' to another character. This eliminates the need for a separate visited array. However, we still need to traverse all cells and perform DFS for each battleship.

**Step 3: Optimized Solution (8 minutes)**

Count only the top-left cell of each battleship: since battleships don't touch each other, we can identify a battleship by its top-left cell (the cell that has no 'X' above it and no 'X' to its left). Iterate through the board, and for each 'X' cell, check if it's a top-left cell. If yes, increment battleship count. This achieves O(m × n) time with O(1) space, which is optimal. The key insight is that we don't need to traverse entire battleships - we can identify them by their top-left corners, which is more efficient.

## Solution Approaches

### Approach 1: Count Top-Left Corners (Optimal)

**Key Insight:** Only count the top-left corner of each battleship. A cell is the top-left corner if:
1. It contains `'X'`
2. The cell above it (if exists) is not `'X'`
3. The cell to the left (if exists) is not `'X'`

**Time Complexity:** O(m × n)  
**Space Complexity:** O(1)

```java
class Solution {
        public int countBattleships(char[][]& board) {
        int count = 0;
        for(int i = 0; i < board.length; i++) {
            for(int j = 0; j < (int)board[0].length; j++) {
                if(board[i].charAt(j) == 'X') {
                    if(i > 0 && board[i - 1][j] == 'X') continue;
                    if(j > 0 && board[i][j - 1] == 'X') continue;
                    count++;
                }
            }
        }
        return count;
    }
}
```

### Approach 2: DFS with Visited Tracking

**Algorithm:**
1. Mark visited battleships to avoid double counting
2. Use DFS to explore each battleship completely
3. Count each battleship only once

**Time Complexity:** O(m × n)  
**Space Complexity:** O(m × n) for visited array

```java
class Solution {
        public int countBattleships(char[][]& board) {
        int m = board.length, n = board[0].length;
        boolean[][] visited(m, boolean[](n, false));
        int count = 0;

        for(int i = 0; i < m; i++) {
            for(int j = 0; j < n; j++) {
                if(board[i].charAt(j) == 'X' && !visited[i][j]) {
                    dfs(board, visited, i, j);
                    count++;
                }
            }
        }
        return count;
    }
    public void dfs(char[][]& board, boolean[][]& visited, int i, int j) {
        if(i < 0 || i >= board.length || j < 0 || j >= board[0].length ||
           board[i].charAt(j) != 'X' || visited[i][j]) return;

        visited[i][j] = true;

        // Explore in all four directions dfs = new directions(board, visited, i + 1, j);
        dfs(board, visited, i - 1, j);
        dfs(board, visited, i, j + 1);
        dfs(board, visited, i, j - 1);
    }
}
```

### Approach 3: Union Find

**Algorithm:**
1. Use Union Find to group connected `'X'` cells
2. Count the number of distinct groups

**Time Complexity:** O(m × n × α(m × n)) where α is inverse Ackermann function  
**Space Complexity:** O(m × n)

```java
// import java.util.*;
class Solution {
        public int countBattleships(char[][]& board) {
        int m = board.length, n = board[0].length;
        UnionFind uf = new UnionFind(m n);
        int count = 0;

        for(int i = 0; i < m; i++) {
            for(int j = 0; j < n; j++) {
                if(board[i].charAt(j) == 'X') {
                    int curr = i n + j;
                    if(i > 0 && board[i - 1][j] == 'X') {
                        uf.unionSets(curr, (i - 1) * n + j);
                    }
                    if(j > 0 && board[i][j - 1] == 'X') {
                        uf.unionSets(curr, i n + (j - 1));
                    }
                }
            }
        }

        HashSet<Integer> roots = new HashSet<Integer>();
        for(int i = 0; i < m; i++) {
            for(int j = 0; j < n; j++) {
                if(board[i].charAt(j) == 'X') {
                    roots.add(uf.find(i n + j));
                }
            }
        }

        return roots.size();
    }
    class UnionFind {
        int[]parent, rank;
        UnionFind(int n) {
            iota(parent /* elements of parent */, 0);
        }
        public int find(int x) {
            if(parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }

        public void unionSets(int x, int y) {
            int px = find(x), py = find(y);
            if(px != py) {
                if(rank[px] < rank[py]) swap(px, py);
                parent[py] = px;
                if(rank[px] == rank[py]) rank.put(px, rank.getOrDefault(px, 0) + 1);
            }
        }
    }
}
```

## Algorithm Analysis

### Top-Left Corner Approach (Recommended)

**Why it works:**
- Each battleship has exactly one top-left corner
- By checking only top and left neighbors, we avoid double counting
- No extra space needed

**Key Conditions:**
```java
if(i > 0 && board[i - 1][j] == 'X') continue;  // Not top-left
if(j > 0 && board[i][j - 1] == 'X') continue;  // Not top-left
```

### Complexity Comparison

| Approach | Time | Space | Pros | Cons |
|----------|------|-------|------|------|
| Top-Left Corner | O(m×n) | O(1) | Optimal, simple | None |
| DFS | O(m×n) | O(m×n) | Clear logic | Extra space |
| Union Find | O(m×n×α) | O(m×n) | Handles complex shapes | Overkill for this problem |

## Key Insights

1. **Battleship Structure**: Each battleship is a connected component of `'X'` cells
2. **No Adjacent Ships**: Ships are separated by at least one empty cell
3. **Top-Left Corner**: Each battleship has exactly one top-left corner
4. **Single Pass**: Can count ships in one pass without modification

## Edge Cases

1. **Empty Board**: Return 0
2. **Single Cell**: `[["X"]]` → 1 battleship
3. **No Battleships**: `[["."]]` → 0 battleships
4. **Large Battleships**: Vertical or horizontal ships of any length

## Follow-up Questions

- What if battleships could be L-shaped or T-shaped?
- How would you find the size of each battleship?
- What if the board could be modified (mark visited ships)?

## Related Problems

- [LC 200: Number of Islands](https://leetcode.com/problems/number-of-islands/)
- [LC 695: Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [LC 130: Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)

## Implementation Notes

1. **Boundary Checks**: Always check array bounds before accessing
2. **Type Casting**: Cast `board.size()` to `int` to avoid comparison warnings
3. **Early Continue**: Use `continue` to skip non-top-left corners
4. **Single Pass**: No need to modify the original board

---

*This problem demonstrates the power of identifying unique characteristics (top-left corners) to solve problems efficiently without extra space.*
