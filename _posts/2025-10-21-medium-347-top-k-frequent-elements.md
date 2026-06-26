---
layout: post
title: "[Medium] 347. Top K Frequent Elements"
date: 2025-10-21 16:00:00 -0700
categories: leetcode medium array hash-table heap
permalink: /posts/2025-10-21-medium-347-top-k-frequent-elements/
tags: [leetcode, medium, array, hash-table, heap, bucket-sort, quickselect]
---

# LC 347: Top K Frequent Elements

**Difficulty:** Medium  
**Category:** Array, Hash Table, Heap, Bucket Sort, Quickselect  
**Companies:** Amazon, Google, Facebook, Microsoft, Apple

## Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in **any order**.

### Examples

**Example 1:**
```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
```

**Example 2:**
```
Input: nums = [1], k = 1
Output: [1]
```

### Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `k` is in the range `[1, the number of unique elements in the array]`
- It is **guaranteed** that the answer is **unique**

## Clarification Questions

Before diving into the solution, here are 5 important clarifications and assumptions to discuss during an interview:

1. **Frequency calculation**: How is frequency calculated? (Assumption: Count occurrences of each element in the array)

2. **Tie-breaking**: When elements have the same frequency, how should we break ties? (Assumption: Return any k elements - order doesn't matter, per problem statement answer is unique)

3. **K validity**: Is k guaranteed to be valid? (Assumption: Yes - per constraints, k is in range [1, number of unique elements])

4. **Return format**: Should we return k elements or all elements with same frequency? (Assumption: Return exactly k elements - top k most frequent)

5. **Element uniqueness**: Can the same element appear multiple times in result? (Assumption: No - each element appears once in the result)

## Interview Deduction Process (20 minutes)

### Step 1: Brute-Force Approach (5 minutes)
**Initial Thought**: "I need to find top k frequent elements. Let me count frequencies and sort."

**Naive Solution**: Count frequency of each element, sort by frequency, return top k elements.

**Complexity**: O(n log n) time, O(n) space

**Issues**:
- O(n log n) time when O(n log k) is possible
- Sorts all elements when only need top k
- Doesn't leverage heap
- Can be optimized

### Step 2: Semi-Optimized Approach (7 minutes)
**Insight**: "I can use min-heap of size k to track top k elements."

**Improved Solution**: Count frequencies, use min-heap of size k. For each element, if heap size < k, add; else if frequency > heap top, replace top.

**Complexity**: O(n log k) time, O(n) space

**Improvements**:
- O(n log k) time is better than O(n log n)
- Heap efficiently maintains top k
- Handles all cases correctly
- Can optimize further

### Step 3: Optimized Solution (8 minutes)
**Final Optimization**: "Min-heap approach is optimal. Can also use bucket sort for specific cases."

**Best Solution**: Min-heap approach is optimal. Count frequencies, use min-heap of size k to maintain top k frequent elements. Alternative: bucket sort if frequency range is small.

**Complexity**: O(n log k) time, O(n) space

**Key Realizations**:
1. Heap is perfect for top-k problems
2. O(n log k) time is optimal for heap approach
3. Min-heap of size k maintains top k efficiently
4. Bucket sort alternative exists for small ranges

## Solution Approaches

### Approach 1: Bucket Sort (Optimal)

**Algorithm:**
1. Count frequency of each element using hash map
2. Create buckets where index represents frequency
3. Iterate buckets from highest to lowest frequency
4. Collect elements until we have k elements

**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        List<List<Integer>> buckets = new ArrayList<>();
        for (int i = 0; i <= nums.length; i++) buckets.add(new ArrayList<>());
        for (var e : freq.entrySet()) buckets.get(e.getValue()).add(e.getKey());
        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.size() - 1; i >= 0 && idx < k; i--) {
            for (int num : buckets.get(i)) {
                result[idx++] = num;
                if (idx == k) return result;
            }
        }
        return result;
    }
}```

### Approach 2: Quickselect

**Algorithm:**
1. Count frequency of each element
2. Create array of unique elements
3. Use quickselect to find k-th largest frequency
4. Return elements with frequencies >= k-th largest

**Time Complexity:** O(n) average, O(n²) worst case  
**Space Complexity:** O(n)

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        List<Integer> unique = new ArrayList<>(freq.keySet());
        quickselect(unique, freq, 0, unique.size() - 1, unique.size() - k);
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = unique.get(unique.size() - k + i);
        return result;
    }

    private void quickselect(List<Integer> arr, Map<Integer, Integer> freq, int l, int r, int k) {
        if (l >= r) return;
        int pivot = l + new Random().nextInt(r - l + 1);
        int p = partition(arr, freq, l, r, pivot);
        if (p == k) return;
        if (k < p) quickselect(arr, freq, l, p - 1, k);
        else quickselect(arr, freq, p + 1, r, k);
    }

    private int partition(List<Integer> arr, Map<Integer, Integer> freq, int l, int r, int pivotIdx) {
        int pivotFreq = freq.get(arr.get(pivotIdx));
        swap(arr, pivotIdx, r);
        int store = l;
        for (int i = l; i < r; i++) {
            if (freq.get(arr.get(i)) < pivotFreq) {
                swap(arr, store, i);
                store++;
            }
        }
        swap(arr, store, r);
        return store;
    }

    private void swap(List<Integer> arr, int i, int j) {
        int tmp = arr.get(i);
        arr.set(i, arr.get(j));
        arr.set(j, tmp);
    }
}```

### Approach 3: Min Heap

**Algorithm:**
1. Count frequency of each element
2. Use min heap of size k to maintain top k frequent elements
3. For each element, if heap size < k, add it
4. If heap size = k and current element has higher frequency than minimum in heap, replace it

**Time Complexity:** O(n log k)  
**Space Complexity:** O(n)

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        for (var e : freq.entrySet()) {
            minHeap.offer(new int[] {e.getValue(), e.getKey()});
            if (minHeap.size() > k) minHeap.poll();
        }
        int[] result = new int[k];
        for (int i = k - 1; i >= 0; i--) result[i] = minHeap.poll()[1];
        return result;
    }
}```

### Approach 4: Max Heap

**Algorithm:**
1. Count frequency of each element
2. Use max heap to store all elements with their frequencies
3. Extract top k elements from heap

**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        for (var e : freq.entrySet()) maxHeap.offer(new int[] {e.getValue(), e.getKey()});
        int[] result = new int[k];
        for (int i = 0; i < k; i++) result[i] = maxHeap.poll()[1];
        return result;
    }
}```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Best When |
|----------|-----------------|------------------|-----------|
| Bucket Sort | O(n) | O(n) | General purpose, optimal |
| Quickselect | O(n) avg, O(n²) worst | O(n) | Large datasets, k ≈ n |
| Min Heap | O(n log k) | O(n) | k << n, memory efficient |
| Max Heap | O(n log n) | O(n) | Simple implementation |

## Key Insights

1. **Bucket Sort Advantage**: Most efficient with O(n) time complexity
2. **Frequency Range**: Maximum frequency is at most n (array length)
3. **Heap Trade-offs**: Min heap better when k is small, max heap simpler but less efficient
4. **Quickselect Optimization**: Good average case but worst case can be O(n²)

## Algorithm Comparison

### Bucket Sort vs Heap Approaches

**Bucket Sort:**
- ✅ O(n) time complexity
- ✅ Simple implementation
- ❌ Uses O(n) extra space for buckets

**Min Heap:**
- ✅ O(n log k) time, good when k << n
- ✅ Memory efficient
- ❌ More complex implementation

**Max Heap:**
- ✅ Simple implementation
- ❌ O(n log n) time complexity
- ❌ Less efficient than min heap

## Follow-up Questions

- What if we need to handle dynamic updates (add/remove elements)?
- How would you optimize for very large datasets that don't fit in memory?
- What if we need the k most frequent elements in sorted order by frequency?

## Related Problems

- [LC 215: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/)
- [LC 973: K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/)
- [LC 692: Top K Frequent Words](https://leetcode.com/problems/top-k-frequent-words/)

## Implementation Notes

1. **Bucket Sort**: Use `int[][]` / `List<List<Integer>>` where index represents frequency
2. **Quickselect**: Random pivot selection for better average performance
3. **Heap**: Use `priority_queue` with custom comparator for min/max heap
4. **Hash Map**: `unordered_map` for O(1) frequency counting

---

*This problem demonstrates the importance of choosing the right algorithm based on constraints and requirements. Bucket sort provides optimal O(n) solution for this specific problem.*
