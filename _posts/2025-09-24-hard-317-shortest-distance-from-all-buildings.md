---
layout: post
title: "[Hard] 317. Shortest Distance from All Buildings"
date: 2025-09-24 19:00:00 -0000
categories: leetcode algorithm bfs graph data-structures matrix shortest-path hard java shortest-distance buildings problem-solving
---

# [Hard] 317. Shortest Distance from All Buildings

<!-- Fixed Liquid syntax error -->

This is a graph traversal problem that requires finding the optimal location to build a new building such that the total distance to all existing buildings is minimized. The key insight is using BFS from each building to calculate distances and finding the spot with minimum total distance.

## Problem Description

Given a 2D grid where:
- `0` represents empty land
- `1` represents a building  
- `2` represents an obstacle

Find the shortest distance from all buildings to a single empty land cell. Return -1 if it's impossible.

### Examples

**Example 1:**
```
Input: grid = [[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]
Output: 7
Explanation: The optimal location is (1,2) with total distance 7.
```

**Example 2:**
```
Input: grid = [[1,0]]
Output: 1
```

**Example 3:**
```
Input: grid = [[1]]
Output: -1
```

### Constraints
- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- grid[i][j] is either 0, 1, or 2
- There will be at least one building in the grid

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **Grid cell types**: What do the values represent? (Assumption: 0 = empty land, 1 = building, 2 = obstacle - cannot pass through)

2. **Distance calculation**: How is distance calculated? (Assumption: Manhattan distance - sum of horizontal and vertical steps, can only move in 4 directions)

3. **Reachability**: Must the empty land be reachable from all buildings? (Assumption: Yes - if cannot reach all buildings, return -1)

4. **Obstacle handling**: Can we pass through obstacles? (Assumption: No - obstacles block movement, cannot build on obstacles)

5. **Return value**: What should we return? (Assumption: Shortest total distance from chosen empty land to all buildings, or -1 if impossible)

## Interview Deduction Process (30 minutes)

### Step 1: Brute-Force Approach (8 minutes)
**Initial Thought**: "I need to find shortest distance. Let me try each empty land position."

**Naive Solution**: For each empty land cell, perform BFS to all buildings, sum distances, find minimum.

**Complexity**: O(m × n × B) time where B is building count, O(m × n) space

**Issues**:
- O(m × n × B) time - inefficient
- Repeats BFS for each empty land
- Doesn't leverage reverse BFS
- Can be optimized significantly

### Step 2: Semi-Optimized Approach (10 minutes)
**Insight**: "I can BFS from each building to all empty lands, accumulate distances."

**Improved Solution**: For each building, perform BFS to all reachable empty lands, accumulate distances. Find empty land with minimum total distance.

**Complexity**: O(B × m × n) time, O(m × n) space

**Improvements**:
- BFS from buildings is more efficient
- Accumulates distances correctly
- Still O(B × m × n) but better structure
- Can optimize further

### Step 3: Optimized Solution (12 minutes)
**Final Optimization**: "BFS from buildings with distance accumulation is optimal. Can optimize with grid modification."

**Best Solution**: BFS from each building, accumulate distances in distance matrix. Use grid modification to track reachability. Find empty land reachable from all buildings with minimum distance.

**Complexity**: O(B × m × n) time, O(m × n) space

**Key Realizations**:
1. BFS from buildings is key insight
2. Distance accumulation enables efficient computation
3. Grid modification tracks reachability
4. O(B × m × n) time is optimal for this approach

## Approach

There are three main approaches to solve this problem:

1. **BFS from Each Empty Land**: For each empty land, BFS to all buildings
2. **BFS from Each Building**: For each building, BFS to all empty lands and accumulate distances
3. **Optimized BFS with Grid Modification**: Use grid values to track reachability

## Solution 1: BFS from Each Empty Land

**Time Complexity:** O(m²n²) - For each empty land, BFS to all buildings  
**Space Complexity:** O(mn) - For visited array and queue

```java
class Solution {
        public int shortestDistance(int[][] grid) {
        int rows = grid.length;
        int cols = grid[0].length;

        int totalHouses = 0;
        for (int row : grid) {
            for (int cell : row) {
                if (cell == 1) totalHouses++;
            }
        }

        int minDistance = Integer.MAX_VALUE;
        for (int r = 0; r < rows; ++r) {
            for (int c = 0; c < cols; ++c) {
                if (grid[r][c] == 0) {
                    minDistance = Math.min(minDistance, bfs(grid, r, c, totalHouses));
                }
            }
        }

        return (minDistance == Integer.MAX_VALUE) ? -1 : minDistance;
    }
        public int bfs(int[][] grid, int startRow, int startCol, int totalHouses) {
        int[][] directions = new int[][] {
            new int[] {1, 0}, new int[] {-1, 0}, new int[] {0, 1}, new int[] {0, -1}
        };
        int rows = grid.length;
        int cols = grid[0].length;

        int distanceSum = 0;
        int housesReached = 0;
        int steps = 0;

        queue<int[]> q;
        q.emplace(startRow, startCol);

        boolean[][] visited(rows, boolean[](cols, false));
        visited[startRow][startCol] = true;

        while (!q.isEmpty() && housesReached != totalHouses) {
            int levelSize = q.size();

            for (int i = 0; i < levelSize; ++i) {
                auto [r, c] = q.get(0);
                q.poll();

                if (grid[r][c] == 1) {
                    distanceSum += steps;
                    ++housesReached;
                    continue;
                }

                for (var e : directions.entrySet()) {
                    int nr = r + dr;
                    int nc = c + dc;

                    if (nr >= 0 && nc >= 0 && nr < rows && nc < cols &&
                        !visited[nr][nc] && grid[nr][nc] != 2) {
                        visited[nr][nc] = true;
                        q.emplace(nr, nc);
                    }
                }
            }
            steps++;
        }

        if (housesReached != totalHouses) {
            for (int r = 0; r < rows; ++r) {
                for (int c = 0; c < cols; ++c) {
                    if (grid[r][c] == 0 && visited[r][c]) {
                        grid[r][c] = 2;  // Mark as unreachable
                    }
                }
            }
            return Integer.MAX_VALUE;
        }

        return distanceSum;
    }
}
```

## Solution 2: BFS from Each Building

**Time Complexity:** O(m²n²) - For each building, BFS to all empty lands  
**Space Complexity:** O(mn) - For distance tracking and visited array

```java
class Solution {
        public int shortestDistance(int[][] grid) {
        int cols = grid[0].length, rows = grid.length;
        int minDisatnce = Integer.MAX_VALUE, totalHouses = 0;
        vector<vector<array<int, 2>>> distances(rows, vector<array<int, 2>> (cols, new int[] {0, 0}));
        for(int row = 0; row < rows; row++) {
            for(int col = 0; col < cols; col++) {
                if(grid[row][col] == 1) {
                    totalHouses++;
                    bfs(grid, distances, row, col);
                }
            }
        }
        for (int row = 0; row < rows; row++) {
            for(int col = 0; col < cols; col++) {
                if(distances[row][col][1] == totalHouses) {
                    minDisatnce = Math.min(minDisatnce, distances[row][col][0]);
                }
            }
        }
        return minDisatnce == Integer.MAX_VALUE ? -1: minDisatnce;
    }
    public void bfs(int[][] grid, vector<vector<array<int, 2>>>& distance, int row, int col) {
        int[][] dirs = new int[][] {
            new int[] {1, 0}, new int[] {-1, 0}, new int[] {0, 1}, new int[] {0, -1}
        };
        int rows = grid.length, cols = grid[0].length;
        queue<int[]> q;
        q.emplace(row, col);
        boolean[][] vis (rows, boolean[](cols, false));
        vis[row][col] = true;
        int steps = 0;
        while(!q.isEmpty()) {
            for (int i = q.size(); i > 0; i--) {
                var cur = q.get(0);
                q.poll();
                row = cur[0];
                col = cur[1];
                if(grid[row][col] == 0) {
                    distance[row][col][0] += steps;
                    distance[row][col][1] += 1;
                }
                for (var e : dirs.entrySet()) {
                    int nextRow = row + dr;
                    int nextCol = col + dc;
                    if (nextRow >= 0 && nextCol >= 0 && nextRow < rows && nextCol < cols) {
                        if(!vis[nextRow][nextCol] && grid[nextRow][nextCol] == 0) {
                            vis[nextRow][nextCol] = true;
                            q.emplace(nextRow, nextCol);
                        }
                    }
                }
            }
            steps++;
        }
    }
}
```

## Solution 3: Optimized BFS with Grid Modification

**Time Complexity:** O(m²n²) - For each building, BFS to all reachable empty lands  
**Space Complexity:** O(mn) - For total distance tracking

```java
class Solution {
        public int shortestDistance(int[][] grid) {
        int rows = grid.length, cols = grid[0].length;
        int[][] dirs = new int[][] {
            new int[] {1, 0}, new int[] {-1, 0}, new int[] {0, 1}, new int[] {0, -1}
        };
        int emptyLandValue =0, minDist = Integer.MAX_VALUE;
        int[][] total = new int[rows][cols];
        for (int row = 0; row < rows; row++) {
            for (int col = 0; col < cols; col++) {
                if(grid[row][col] == 1) {
                    minDist = Integer.MAX_VALUE;
                    queue<int[]> q;
                    q.emplace(row, col);
                    int steps = 0;
                    while(!q.isEmpty()) {
                        steps++;
                        for(int level = q.size(); level > 0; level--) {
                            var cur = q.get(0);
                            q.poll();
                            for (var e : dirs.entrySet()) {
                                int nextRow = cur[0] + dr;
                                int nextCol = cur[1] + dc;
                                if(nextRow >= 0 && nextRow < rows && nextCol >= 0 && nextCol < cols
                                && grid[nextRow][nextCol] == emptyLandValue){
                                    grid[nextRow][nextCol]--;
                                    total[nextRow][nextCol] += steps;
                                    q.emplace(nextRow, nextCol);
                                    minDist = Math.min(minDist, total[nextRow][nextCol]);
                                }
                            }
                        }
                    }
                    emptyLandValue--;
                }
            }
        }
        return minDist == Integer.MAX_VALUE ? -1 : minDist;
    }
}
```

## Step-by-Step Example

Let's trace through Solution 2 with grid = `[[1,0,2,0,1],[0,0,0,0,0],[0,0,1,0,0]]`:

**Step 1:** Count total houses = 3

**Step 2:** BFS from each building
- Building at (0,0): Updates distances to all reachable empty lands
- Building at (0,4): Updates distances to all reachable empty lands  
- Building at (2,2): Updates distances to all reachable empty lands

**Step 3:** Check each empty land
- Only empty lands reachable by all 3 buildings are considered
- Find minimum total distance among valid positions

**Result:** Position (1,2) with total distance 7

## Key Insights

1. **BFS Level Processing**: Process each level of BFS to calculate distances correctly
2. **Reachability Check**: Ensure all buildings can reach the chosen empty land
3. **Distance Accumulation**: Sum distances from all buildings to each empty land
4. **Grid Optimization**: Use grid modification to track reachability efficiently

## Approach Comparison

| Approach | Pros | Cons |
|----------|------|------|
| **Solution 1** | Simple logic, easy to understand | Less efficient, modifies original grid |
| **Solution 2** | Clean separation, tracks reachability | Uses extra space for distance tracking |
| **Solution 3** | Most efficient, reuses grid space | Complex logic, harder to debug |

## Common Mistakes

- **Incorrect Distance Calculation**: Not using level-by-level BFS
- **Reachability Issues**: Not checking if all buildings can reach empty land
- **Grid Modification**: Modifying original grid without proper restoration
- **Boundary Conditions**: Not handling edge cases properly

---
