---

layout: post
title: "[Medium] 794. Valid Tic-Tac-Toe State"
date: 2025-09-24 17:00:00 -0000
categories: leetcode algorithm simulation data-structures game-logic validation medium java tic-tac-toe game-validation problem-solving
permalink: /posts/2025-09-24-medium-794-valid-tic-tac-toe-state/
---

{% raw %}
This is a simulation problem that requires understanding the rules of Tic-Tac-Toe and validating whether a given board state is possible. The key insight is checking the count of X's and O's, and ensuring that winning conditions are valid.

Given a Tic-Tac-Toe board as an array of strings, return whether this board state is valid.

A Tic-Tac-Toe board is valid if:
1. The number of X's and O's follows the game rules
2. Only one player can win
3. If X wins, there should be exactly one more X than O
4. If O wins, there should be equal number of X's and O's

## Examples
**Example 1:**
```
Input: board = ["O  ","   ","   "]
Output: false
Explanation: The first player always plays "X".
```

**Example 2:**
```
Input: board = ["XOX"," X ","   "]
Output: false
Explanation: Players take turns making moves.
```

**Example 3:**
```
Input: board = ["XXX","   ","OOO"]
Output: false
Explanation: Both players win at the same time.
```

## Constraints
- board.length == 3
- board[i].length == 3
- board[i][j] is either 'X', 'O', or ' '

## Thinking Process

The solution involves checking several conditions:

1. **Count Validation**: Count X's and O's - X should have equal or one more count than O
2. **Win Detection**: Check if either player has won (rows, columns, diagonals)
3. **Win Validation**: 
   - If X wins, O should have exactly one less count than X
   - If O wins, X and O should have equal counts
   - Both players cannot win simultaneously

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 230 110" style="max-width:100%;height:auto;display:block;margin:1.5em auto;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif">
<text x="50%" y="18" text-anchor="middle" font-size="13" font-weight="600" fill="#5A5752">Array + hash map</text>

  <rect x="30" y="45" width="28" height="28" rx="3" fill="#E8E3D8" stroke="#B8B5B0"/><text x="44" y="61" text-anchor="middle" font-size="10">2</text>
  <rect x="62" y="45" width="28" height="28" rx="3" fill="#E0D8E4" stroke="#A098A8"/><text x="76" y="61" text-anchor="middle" font-size="10">7</text>
  <rect x="106" y="45" width="28" height="28" rx="3" fill="#E8E3D8" stroke="#B8B5B0"/><text x="120" y="61" text-anchor="middle" font-size="10">11</text>
  <rect x="150" y="40" width="60" height="38" rx="4" fill="#FAF8F5" stroke="#D4D1CC"/>
  <text x="180" y="61" text-anchor="middle" font-size="10" fill="#6B6560">map</text>
  <text x="110" y="100" text-anchor="middle" font-size="11" fill="#6B6560">hash map for O(1) lookups</text>

</svg>

## Common Approaches

Typical techniques for this pattern:

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| **Brute force** *(this problem)* | Often O(n^2) or O(2^n) | O(n) | Baseline; clarifies the optimization target |
| Sort + scan | O(n log n) | O(1) | Pairs, intervals, greedy ordering |
| Hash map / set | O(n) | O(n) | Frequency, membership, two-sum style |
| Single-pass linear | O(n) | O(1) | Two pointers, sliding window, Kadane |

## Solution
**Time Complexity:** O(1) - Constant time since board is always 3x3  
**Space Complexity:** O(1) - Only using constant extra space

```java
class Solution {
    public boolean validTicTacToe(String[] board) {
        int x = 0, o = 0;
        for (String row : board) {
            for (char c : row.toCharArray()) {
                if (c == 'X') x++;
                if (c == 'O') o++;
            }
        }
        if (x != o && x != o + 1) return false;
        boolean xWin = win(board, 'X');
        boolean oWin = win(board, 'O');
        if (xWin && o != x - 1) return false;
        if (oWin && o != x) return false;
        return !(xWin && oWin);
    }

    private boolean win(String[] board, char p) {
        for (int i = 0; i < 3; i++) {
            if (board[i].charAt(0) == p && board[i].charAt(1) == p && board[i].charAt(2) == p) return true;
            if (board[0].charAt(i) == p && board[1].charAt(i) == p && board[2].charAt(i) == p) return true;
        }
        if (board[0].charAt(0) == p && board[1].charAt(1) == p && board[2].charAt(2) == p) return true;
        if (board[0].charAt(2) == p && board[1].charAt(1) == p && board[2].charAt(0) == p) return true;
        return false;
    }
}```

### Solution Explanation

**Approach:** Brute force (this problem)

**Key idea:** The solution involves checking several conditions:

**How the code works:**
1. **Count Validation**: Count X's and O's - X should have equal or one more count than O
2. **Win Detection**: Check if either player has won (rows, columns, diagonals)
3. **Win Validation**:
- If X wins, O should have exactly one less count than X
- If O wins, X and O should have equal counts
- Both players cannot win simultaneously

**Walkthrough** — input `board = ["O  ","   ","   "]`, expected output `false`:

The first player always plays "X".
## Step-by-Step Example

Let's trace through the solution with board = `["XOX"," X ","OOO"]`:

**Step 1:** Count X's and O's
- X count: 3 (positions: (0,0), (0,2), (1,1))
- O count: 3 (positions: (0,1), (2,0), (2,1), (2,2))
- Check: `x_cnt != o_cnt + 1 && x_cnt != o_cnt` → `3 != 4 && 3 != 3` → `true && false` → `false` ✓

**Step 2:** Check for wins
- X wins: Check rows, columns, diagonals → No win for X
- O wins: Row 2 has all O's → O wins ✓

**Step 3:** Validate win conditions
- O wins and `o_cnt != x_cnt` → `3 != 3` → `false` ✓
- Both X and O don't win simultaneously ✓

**Result:** Valid board state

## Common Mistakes

- Not checking if both players win simultaneously
- Incorrect count validation (allowing O to have more pieces than X)
- Missing diagonal win conditions
- Not handling edge cases like empty boards

---

## References

- [LC 794: Valid Tic-Tac-Toe State on LeetCode](https://leetcode.com/problems/valid-tic-tac-toe-state/)
- [LeetCode Discuss — LC 794: Valid Tic-Tac-Toe State](https://leetcode.com/problems/valid-tic-tac-toe-state/discuss/)
- [LeetCode Editorial](https://leetcode.com/problems/valid-tic-tac-toe-state/editorial/) *(may require premium)*

## Key Takeaways

1. **Turn Order**: X always goes first, so X should have equal or one more count than O
2. **Win Detection**: Check all rows, columns, and both diagonals
3. **Mutual Exclusivity**: Only one player can win in a valid game
4. **Count Validation**: Winning player must have the correct count based on game rules
{% endraw %}
