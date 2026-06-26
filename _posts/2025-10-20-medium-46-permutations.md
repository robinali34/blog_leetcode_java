---
layout: post
title: "[Medium] 46. Permutations"
date: 2025-10-20 14:00:00 -0700
categories: leetcode algorithm medium backtracking recursion
permalink: /2025/10/20/medium-46-permutations/
---

# 46. Permutations

**Difficulty:** Medium  
**Category:** Backtracking, Recursion

## Problem Statement

Given an array `nums` of distinct integers, return **all the possible permutations**. You can return the answer in **any order**.

## Examples

### Example 1:
```
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Example 2:
```
Input: nums = [0,1]
Output: [[0,1],[1,0]]
```

### Example 3:
```
Input: nums = [1]
Output: [[1]]
```

## Constraints

- `1 <= nums.length <= 6`
- `-10 <= nums[i] <= 10`
- All the integers of `nums` are **unique**.

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **Permutation definition**: What is a permutation? (Assumption: All possible arrangements of array elements - order matters)

2. **Element uniqueness**: Are all elements unique? (Assumption: Yes - per constraints, all integers are unique)

3. **Output format**: Should we return all permutations or just count? (Assumption: Return all distinct permutations - list of lists)

4. **Array modification**: Can we modify the input array? (Assumption: Typically yes for backtracking, but should clarify)

5. **Empty array**: What if array is empty? (Assumption: Return [[]] - one permutation with no elements)

## Interview Deduction Process (20 minutes)

**Step 1: Brute-Force Approach (5 minutes)**

Generate all possible arrangements by trying all positions for each element. Use nested loops or recursive generation without pruning. This approach works but generates duplicates and has exponential complexity. The challenge is ensuring all permutations are generated exactly once.

**Step 2: Semi-Optimized Approach (7 minutes)**

Use backtracking: build permutations incrementally. For each position, try each unused element. Use a visited set or boolean array to track which elements have been used. When permutation is complete (all positions filled), add to results. Backtrack by unmarking elements. This avoids duplicates but still explores all possibilities.

**Step 3: Optimized Solution (8 minutes)**

Use backtracking with in-place swapping. Instead of maintaining a separate array and visited set, swap elements in the original array. For position i, swap elements at positions i and j (where j >= i), recursively generate permutations for position i+1, then swap back. This achieves O(n! × n) time (n! permutations, each taking O(n) to build) with O(n) space for recursion stack. The key insight is that swapping allows us to use the array itself to track the current permutation state, eliminating the need for extra visited tracking.

## Approach

This is a classic **backtracking** problem that requires generating all possible permutations of a given array. There are two main approaches:

1. **Backtracking with Swapping:** Generate permutations by swapping elements in-place
2. **permutation generation (library or backtracking):** Use Java Collections' built-in permutation generator

### Algorithm 1: Backtracking with Swapping
1. **Start from index 0** and try each element at current position
2. **Swap elements** to place them at current position
3. **Recursively generate** permutations for remaining positions
4. **Backtrack** by swapping back to original positions
5. **Base case:** When we've placed all elements, add current permutation

### Algorithm 2: permutation generation (library or backtracking)
1. **Sort the array** to get lexicographically smallest permutation
2. **Use do-while loop** with `next_permutation()` to generate all permutations
3. **Add each permutation** to result vector
4. **Continue until** no more permutations exist

## Solution

### Solution 1: Backtracking with Swapping

```java
class Solution {
    public int[][] permute(int[] nums) {
        List<int[]> rtn = new ArrayList<>();
        permute(nums, 0, rtn);
        return rtn;
    }
    public void permute(int[] nums, int idx, int[][] rtn) {
        if(idx == nums.length) {
            rtn.add(nums);
            return;
        }
        for(int i = idx; i < nums.length; i++) {
            swap(nums, idx, i);
            permute(nums, idx + 1, rtn);
            swap(nums, idx, i);
        }
    }
}
```

### Solution 2: permutation generation (library or backtracking)

```java
// import java.util.Arrays;
// import java.util.Collections;
class Solution {
    public int[][] permute(int[] nums) {
        List<int[]> rtn = new ArrayList<>();
        Arrays.sort(nums);
        do{
            rtn.add(nums);
        } while(next_permutation(nums /* elements of nums */));
        return rtn;
    }
}
```

## Explanation

### Solution 1: Backtracking with Swapping

**Step-by-Step Process:**

1. **Base Case:** When `idx == nums.size()`, we've generated a complete permutation
2. **Recursive Case:** For each position `idx`, try every element from `idx` to `n-1`
3. **Swap:** Place element at position `i` to position `idx`
4. **Recurse:** Generate permutations for remaining positions (`idx + 1`)
5. **Backtrack:** Swap back to restore original state

**Example Walkthrough for `nums = [1,2,3]`:**

```
Initial: [1,2,3], idx=0
├─ Swap(0,0): [1,2,3] → Recurse with idx=1
│  ├─ Swap(1,1): [1,2,3] → Recurse with idx=2
│  │  └─ Swap(2,2): [1,2,3] → idx=3, add [1,2,3]
│  └─ Swap(1,2): [1,3,2] → Recurse with idx=2
│     └─ Swap(2,2): [1,3,2] → idx=3, add [1,3,2]
├─ Swap(0,1): [2,1,3] → Recurse with idx=1
│  ├─ Swap(1,1): [2,1,3] → Recurse with idx=2
│  │  └─ Swap(2,2): [2,1,3] → idx=3, add [2,1,3]
│  └─ Swap(1,2): [2,3,1] → Recurse with idx=2
│     └─ Swap(2,2): [2,3,1] → idx=3, add [2,3,1]
└─ Swap(0,2): [3,2,1] → Recurse with idx=1
   ├─ Swap(1,1): [3,2,1] → Recurse with idx=2
   │  └─ Swap(2,2): [3,2,1] → idx=3, add [3,2,1]
   └─ Swap(1,2): [3,1,2] → Recurse with idx=2
      └─ Swap(2,2): [3,1,2] → idx=3, add [3,1,2]
```

### Solution 2: permutation generation (library or backtracking)

**Step-by-Step Process:**

1. **Sort array** to get lexicographically smallest permutation
2. **Generate permutations** using `next_permutation()` in do-while loop
3. **Add each permutation** to result vector
4. **Continue until** `next_permutation()` returns false

**Example Walkthrough for `nums = [1,2,3]`:**

```
Sorted: [1,2,3]
1. [1,2,3] → Add to result
2. [1,3,2] → Add to result  
3. [2,1,3] → Add to result
4. [2,3,1] → Add to result
5. [3,1,2] → Add to result
6. [3,2,1] → Add to result
7. next_permutation returns false → Stop
```

## Complexity Analysis

### Solution 1: Backtracking with Swapping
**Time Complexity:** O(n! × n)
- **Permutations:** n! permutations generated
- **Each permutation:** O(n) time to copy array
- **Total:** O(n! × n)

**Space Complexity:** O(n)
- **Recursion depth:** O(n) for the call stack
- **No additional space** for storing permutations during generation

### Solution 2: permutation generation (library or backtracking)
**Time Complexity:** O(n! × n)
- **Permutations:** n! permutations generated
- **Each permutation:** O(n) time for `next_permutation()` and copying
- **Total:** O(n! × n)

**Space Complexity:** O(1)
- **No recursion:** Iterative approach
- **No additional space** beyond input and output

## Key Insights

1. **Backtracking Pattern:** Classic recursive approach with state restoration
2. **In-place Generation:** Swapping allows generating permutations without extra space
3. **Library efficiency:** `next_permutation()` is highly optimized
4. **Lexicographic Order:** library approach generates permutations in sorted order
5. **State Management:** Proper backtracking ensures all possibilities are explored

## Comparison of Approaches

| Approach | Time | Space | Advantages | Disadvantages |
|----------|------|-------|------------|---------------|
| **Backtracking** | O(n! × n) | O(n) | Educational, flexible | Recursive overhead |
| **Library** | O(n! × n) | O(1) | Concise, optimized | Less control over order |

## Alternative Approaches

### Approach 3: Backtracking with Visited Array
```java
class Solution {
    public int[][] permute(int[] nums) {
        List<int[]> result = new ArrayList<>();
        List<Integer> current = new ArrayList<>();
        boolean[]used(nums.length, false);
        backtrack(nums, current, used, result);
        return result;
    }
    public void backtrack(int[] nums, int[] current,
                   boolean[] used, int[][] result) {
        if(current.size() == nums.length) {
            result.add(current);
            return;
        }

        for(int i = 0; i < nums.length; i++) {
            if(used[i]) continue;

            used[i] = true;
            current.add(nums[i]);
            backtrack(nums, current, used, result);
            current.removeLast();
            used[i] = false;
        }
    }
}
```

### Approach 4: Iterative with Stack
```java
class Solution {
    public int[][] permute(int[] nums) {
        List<int[]> result = new ArrayList<>();
        stack<int[]> stk;
        stk.offer({});

        while(!stk.isEmpty()) {
            int[]current = stk.peek();
            stk.poll();

            if(current.size() == nums.length) {
                result.add(current);
                continue;
            }

            for(int num : nums) {
                if(find(current /* elements of current */, num) == current.iterator()) {
                    int[]next = current;
                    next.add(num);
                    stk.offer(next);
                }
            }
        }

        return result;
    }
}
```

## When to Use Each Approach

### Use Backtracking with Swapping when:
- **Memory is limited** (O(n) space vs O(n!) for visited approach)
- **Need to understand** the algorithm deeply
- **Custom modifications** are required

### Use permutation generation (library or backtracking) when:
- **Code simplicity** is priority
- **Lexicographic order** is desired
- **Performance** is critical (highly optimized)

### Use Visited Array when:
- **Clarity** is more important than space
- **Need to track** which elements are used
- **Modifying** the original array is not allowed

## Key Concepts

1. **Permutations:** All possible arrangements of elements
2. **Backtracking:** Systematic exploration with state restoration
3. **Recursion:** Divide problem into smaller subproblems
4. **State Space:** All possible configurations to explore
5. **Pruning:** Avoiding invalid or duplicate states

This problem is fundamental for understanding backtracking algorithms and is commonly used in interviews to test recursive thinking and state management skills.
