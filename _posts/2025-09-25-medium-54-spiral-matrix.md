---
layout: post
title: "[Medium] 54. Spiral Matrix"
categories: leetcode algorithm matrix data-structures simulation traversal medium java spiral-matrix problem-solving
---

# [Medium] 54. Spiral Matrix

Given an m x n matrix, return all elements of the matrix in spiral order.

## Examples

**Example 1:**
```
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]
```

**Example 2:**
```
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]
```

## Constraints

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **Spiral direction**: What is the spiral order? (Assumption: Right → Down → Left → Up, repeating - clockwise spiral)

2. **Matrix shape**: Can the matrix be non-square (rectangular)? (Assumption: Yes - m and n can be different)

3. **Output format**: Should we return elements in spiral order? (Assumption: Yes - return 1D array with elements in spiral traversal order)

4. **Empty matrix**: How should we handle an empty matrix? (Assumption: Return empty array)

5. **Visited tracking**: Can we modify the matrix or need separate tracking? (Assumption: Can use visited array or modify matrix values to mark visited)

## Interview Deduction Process (20 minutes)

### Step 1: Brute-Force Approach (5 minutes)
**Initial Thought**: "I need to traverse matrix in spiral. Let me try all directions manually."

**Naive Solution**: Manually track current position and direction, move step by step, check boundaries manually.

**Complexity**: O(m × n) time, O(m × n) space

**Issues**:
- Complex boundary checking
- Error-prone direction changes
- Doesn't leverage systematic approach
- Hard to handle edge cases

### Step 2: Semi-Optimized Approach (7 minutes)
**Insight**: "I can use direction vectors and visited tracking. When hit boundary or visited cell, change direction."

**Improved Solution**: Use direction vectors [right, down, left, up]. Track visited cells. Move in current direction until boundary or visited cell, then change direction.

**Complexity**: O(m × n) time, O(m × n) space

**Improvements**:
- Systematic direction handling
- Cleaner boundary checking
- Handles all cases correctly
- Still uses visited array

### Step 3: Optimized Solution (8 minutes)
**Final Optimization**: "Can use boundary tracking instead of visited array to save space."

**Best Solution**: Track boundaries (top, bottom, left, right). Traverse right, then down, then left, then up, updating boundaries after each direction. This avoids visited array.

**Complexity**: O(m × n) time, O(1) space

**Key Realizations**:
1. Boundary tracking avoids visited array
2. O(m × n) time is optimal - must visit each cell
3. O(1) space is optimal with boundary tracking
4. Direction vectors make code cleaner

## Approach

There are two main approaches to solve this problem:

1. **Boundary Tracking**: Use four boundaries (top, bottom, left, right) and traverse in spiral order
2. **Direction Simulation**: Use direction vectors and mark visited cells to simulate spiral movement

## Solution 1: Boundary Tracking Approach

```java
class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> result = new ArrayList<>();
        if (matrix.length == 0) return result;
        int top = 0, bottom = matrix.length - 1, left = 0, right = matrix[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) result.add(matrix[top][j]);
            top++;
            for (int i = top; i <= bottom; i++) result.add(matrix[i][right]);
            right--;
            if (top <= bottom) {
                for (int j = right; j >= left; j--) result.add(matrix[bottom][j]);
                bottom--;
            }
            if (left <= right) {
                for (int i = bottom; i >= top; i--) result.add(matrix[i][left]);
                left++;
            }
        }
        return result;
    }
}```

**Time Complexity:** O(m × n) - Visit each cell exactly once
**Space Complexity:** O(1) - Only using variables for boundaries

## Solution 2: Direction Simulation Approach

{% raw %}
```java
class Solution {
    public int[] spiralOrder(int[][] matrix) {
        if(matrix.length == 0 || matrix[0].length == 0) return {}
        int ROWS = matrix.length, COLS = matrix[0].length;
        boolean[][] visited(ROWS, boolean[](COLS, false));
        int TOTAL = ROWS COLS;
        int[] order = new int[TOTAL];

        int row = 0, col = 0;
        int dirIdx = 0;
        for(int i = 0; i < TOTAL; i++) {
            order[i] = matrix[row][col];
            visited[row][col] = true;
            int nextRow = row + DIRS[dirIdx][0], nextCol = col + DIRS[dirIdx][1];
            if(nextRow < 0 || nextRow >= ROWS || nextCol < 0 || nextCol >= COLS || visited[nextRow][nextCol]) {
                dirIdx = (dirIdx + 1) % 4;
            }
            row += DIRS[dirIdx][0];
            col += DIRS[dirIdx][1];
        }
        return order;
    }
    int[][] DIRS = {new int[] {0, 1}, new int[] {1, 0}, {0, -1}, {-1, 0}}
}
```
{% endraw %}

**Time Complexity:** O(m × n) - Visit each cell exactly once
**Space Complexity:** O(m × n) - Visited matrix plus output array

## Step-by-Step Example (Solution 1)

For matrix = [[1,2,3],[4,5,6],[7,8,9]]:

1. **Initial boundaries:** up=0, down=2, left=0, right=2
2. **Right traversal:** [1,2,3] → rtn = [1,2,3]
3. **Down traversal:** [6,9] → rtn = [1,2,3,6,9]
4. **Left traversal:** [8,7] → rtn = [1,2,3,6,9,8,7]
5. **Up traversal:** [4] → rtn = [1,2,3,6,9,8,7,4]
6. **Update boundaries:** up=1, down=1, left=1, right=1
7. **Right traversal:** [5] → rtn = [1,2,3,6,9,8,7,4,5]

Final result: [1,2,3,6,9,8,7,4,5]

## Key Insights

1. **Boundary Management**: Track four boundaries and move them inward after each complete spiral
2. **Edge Cases**: Handle single row/column matrices with conditional checks
3. **Direction Changes**: Use direction vectors to simulate spiral movement
4. **Visited Marking**: Mark cells as visited to avoid revisiting them

## Solution Comparison

- **Boundary Tracking**: More intuitive, doesn't modify input matrix, cleaner logic
- **Direction Simulation**: More general approach, can be extended to other spiral problems

## Common Mistakes

1. **Off-by-one errors** in boundary conditions
2. **Not handling single row/column** cases properly
3. **Incorrect boundary updates** after each spiral
4. **Missing edge cases** for 1x1 matrices

## Related Problems

- [59. Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/)
- [885. Spiral Matrix III](https://leetcode.com/problems/spiral-matrix-iii/)
- [2326. Spiral Matrix IV](https://leetcode.com/problems/spiral-matrix-iv/)
