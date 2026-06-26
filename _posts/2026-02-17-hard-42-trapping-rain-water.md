---
layout: post
title: "[Hard] 42. Trapping Rain Water"
date: 2026-02-17
categories: [leetcode, hard, two-pointers, stack, dp]
tags: [leetcode, hard, two-pointers, monotonic-stack, prefix-suffix, dp]
permalink: /2026/02/17/hard-42-trapping-rain-water/
---

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

## Examples

**Example 1:**

```
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

**Example 2:**

```
Input: height = [4,2,0,3,2,5]
Output: 9
```

## Constraints

- `n == height.length`
- `1 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

## Thinking Process

### Mathematical Model

At index `i`, the water trapped is:

$$\text{water}[i] = \min(\text{maxLeft}[i],\ \text{maxRight}[i]) - \text{height}[i]$$

If negative, clamp to 0. Where:
- `maxLeft[i]` = maximum height from `0` to `i`
- `maxRight[i]` = maximum height from `i` to `n-1`

### From Brute Force to Optimal

**Brute force**: For each index, scan left and right to find the max. $O(n^2)$ -- too slow.

**Prefix/Suffix arrays**: Precompute `leftMax[]` and `rightMax[]` in two passes. $O(n)$ time, $O(n)$ space. Safe and clean.

**Two pointers**: Key insight -- if `leftMax < rightMax`, water depends **only** on `leftMax` because $\min(\text{leftMax}, \text{rightMax}) = \text{leftMax}$. The opposite side is guaranteed to be at least as tall. So we don't need full arrays; just move the smaller side inward. $O(n)$ time, $O(1)$ space.

### Comparison Table

| Approach | Time | Space | Notes |
|---|---|---|---|
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Prefix/Suffix | $O(n)$ | $O(n)$ | Safe, easy |
| Two Pointers | $O(n)$ | $O(1)$ | Optimal |
| Monotonic Stack | $O(n)$ | $O(n)$ | Useful pattern |

## Approach 1: Brute Force -- $O(n^2)$

For each index, scan left and right to find the max height on each side.

{% raw %}
```java
class Solution {
        public int trap(int[] height) {
        int n = height.size();
        int water = 0;

        for (int i = 0; i < n; i++) {
            int leftMax = 0, rightMax = 0;

            for (int l = 0; l <= i; l++)
                leftMax = Math.max(leftMax, height[l]);

            for (int r = i; r < n; r++)
                rightMax = Math.max(rightMax, height[r]);

            water += Math.min(leftMax, rightMax) - height[i];
        }

        return water;
    }
}
```
{% endraw %}

**Time**: $O(n^2)$
**Space**: $O(1)$

## Approach 2: Prefix & Suffix Arrays -- $O(n)$ time, $O(n)$ space

Precompute `leftMax[i]` and `rightMax[i]` in two linear passes, then compute water in a third pass.

{% raw %}
```java
class Solution {
        public int trap(int[] height) {
        int n = height.size();
        if (n == 0) return 0;

        int[] leftMax = new int[n], rightMax(n);
        int water = 0;

        leftMax[0] = height[0];
        for (int i = 1; i < n; i++)
            leftMax[i] = Math.max(leftMax[i - 1], height[i]);

        rightMax[n - 1] = height[n - 1];
        for (int i = n - 2; i >= 0; i--)
            rightMax[i] = Math.max(rightMax[i + 1], height[i]);

        for (int i = 0; i < n; i++)
            water += Math.min(leftMax[i], rightMax[i]) - height[i];

        return water;
    }
}
```
{% endraw %}

**Time**: $O(n)$
**Space**: $O(n)$

## Approach 3: Two Pointers -- $O(n)$ time, $O(1)$ space (Optimal)

The smaller side always determines the bottleneck. Move the pointer on the smaller side inward, accumulating water as you go.

**Invariant**: At each step, the smaller of `leftMax` and `rightMax` determines trapped water. Since the opposite side is guaranteed $\geq$ the smaller side, the water calculation is always safe.

{% raw %}
```java
class Solution {
        public int trap(int[] height) {
        int n = height.size();
        if (n == 0) return 0;

        int l = 0, r = n - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        while (l < r) {
            if (height[l] < height[r]) {
                if (height[l] >= leftMax)
                    leftMax = height[l];
                else
                    water += leftMax - height[l];
                l++;
            } else {
                if (height[r] >= rightMax)
                    rightMax = height[r];
                else
                    water += rightMax - height[r];
                r--;
            }
        }

        return water;
    }
}
```
{% endraw %}

**Time**: $O(n)$
**Space**: $O(1)$

## Approach 4: Monotonic Stack -- $O(n)$ time, $O(n)$ space

Process bars left to right. When a taller bar is found, pop shorter bars from the stack and compute the water trapped in the "valley" between the current bar and the new stack top.

{% raw %}
```java
// import java.util.*;
class Solution {
        public int trap(int[] height) {
        int n = height.size();
        int water = 0;
        Deque<Integer> st = new ArrayDeque<>();

        for (int i = 0; i < n; i++) {
            while (!st.isEmpty() && height[i] > height[st.peek()]) {
                int top = st.peek();
                st.poll();

                if (st.length == 0) break;

                int distance = i - st.peek() - 1;
                int boundedHeight = Math.min(height[i], height[st.peek()]) - height[top];
                water += distance boundedHeight;
            }
            st.offer(i);
        }

        return water;
    }
}
```
{% endraw %}

**Time**: $O(n)$ -- each index is pushed and popped at most once
**Space**: $O(n)$ for the stack

## Pattern Recognition

When you see "for each position, need left info + right info," immediately consider:
- **Prefix/suffix arrays** -- safe and straightforward
- **Two pointers** -- optimal when one side dominates
- **Monotonic stack** -- when the problem involves bounded areas between bars

## Key Takeaways

- The formula $\min(\text{maxLeft}, \text{maxRight}) - \text{height}$ is the foundation -- all four approaches implement it differently
- Two pointers eliminates extra space by observing that the smaller side is the only bottleneck
- Monotonic stack computes water layer by layer (horizontally) rather than column by column (vertically)
- Master both two-pointer and monotonic-stack versions -- they appear in many related problems

## Related Problems

- [11. Container With Most Water](https://leetcode.com/problems/container-with-most-water/) -- two-pointer on water area
- [84. Largest Rectangle in Histogram](https://leetcode.com/problems/largest-rectangle-in-histogram/) -- monotonic stack classic
- [407. Trapping Rain Water II](https://leetcode.com/problems/trapping-rain-water-ii/) -- 3D version with BFS + heap

## Template Reference

- [Stack](/blog_leetcode_java/posts/2025-11-13-leetcode-templates-stack/)
- [Data Structures](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
