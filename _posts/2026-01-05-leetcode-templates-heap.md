---
layout: post
title: "Algorithm Templates: Heap"
date: 2026-01-05 00:00:00 -0700
categories: leetcode templates heap priority-queue
permalink: /posts/2026-01-05-leetcode-templates-heap/
tags: [leetcode, templates, heap, priority-queue, data-structures]
---

{% raw %}
Minimal, copy-paste Java for min/max heap, K-way merge, top K, and two heaps. See also [Data Structures](/posts/2025-10-29-leetcode-templates-data-structures/) for heap patterns.

## Contents

- [Heap Overview](#heap-overview)
- [Min Heap](#min-heap)
- [Max Heap](#max-heap)
- [Custom Comparators](#custom-comparators)
- [Common Patterns](#common-patterns)
- [K-way Merge](#k-way-merge)
- [Top K Elements](#top-k-elements)
- [Two Heaps](#two-heaps)
- [Dijkstra's Algorithm](#dijkstras-algorithm)

## Heap Overview

A **heap** (priority queue) is a complete binary tree that satisfies the heap property:
- **Min Heap**: Parent node is always less than or equal to its children
- **Max Heap**: Parent node is always greater than or equal to its children

**Key Operations:**
- `push(x)`: Insert element - O(log n)
- `pop()`: Remove top element - O(log n)
- `top()`: Access top element - O(1)
- `empty()`: Check if empty - O(1)
- `size()`: Get size - O(1)

**Use Cases:**
- Finding K largest/smallest elements
- Merging K sorted sequences
- Maintaining running median
- Shortest path algorithms (Dijkstra's)
- Scheduling problems

## Min Heap

Min heap keeps the smallest element at the top.

```java
// Min heap (smallest element at top) - using greater<>
priority_queue<int, int[], greater<int>> minHeap;

// Min heap using `PriorityQueue` with comparator
priority_queue<int, int[], greater<>> minHeap2;

// Min heap using lambda comparator (decltype required)
var minCmp = [](int a, int b) { return a > b; }
priority_queue<int, int[], decltype(minCmp)> minHeap3(minCmp);

// Note: decltype is REQUIRED for lambdas because each lambda has a unique type
// You cannot use: priority_queue<int, int[], [](auto a, auto b) { return a > b; }>  // ❌ Invalid

// Basic operations
minHeap.push(5);
minHeap.push(2);
minHeap.push(8);
minHeap.push(1);

minHeap.top();    // Returns 1 (smallest)
minHeap.pop();    // Removes 1
minHeap.top();    // Returns 2 (next smallest)
```

### Example: Find K Smallest Elements

```java
int[]findKSmallest(int[] nums, int k) {
    priority_queue<int, int[], greater<int>> minHeap;

    for(int num : nums) {
        minHeap.push(num);
    }

    int[]result;
    for(int i = 0; i < k && !minHeap.length == 0; i++) {
        result.add(minHeap.top());
        minHeap.pop();
    }

    return result;
}
```

## Max Heap

Max heap keeps the largest element at the top (default in Java).

```java
// import java.util.*;

// Max heap (largest element at top) - default
PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>();

// Max heap explicitly using less<> (default comparator)
priority_queue<int, int[], less<int>> maxHeap2;

// Max heap using lambda comparator (decltype required)
var maxCmp = [](int a, int b) { return a < b; }
priority_queue<int, int[], decltype(maxCmp)> maxHeap3(maxCmp);

// Note: decltype is REQUIRED for lambdas because each lambda has a unique type
// You cannot use: priority_queue<int, int[], [](auto a, auto b) { return a < b; }>  // ❌ Invalid

// Basic operations
maxHeap.push(5);
maxHeap.push(2);
maxHeap.push(8);
maxHeap.push(1);

maxHeap.top();    // Returns 8 (largest)
maxHeap.pop();    // Removes 8
maxHeap.top();    // Returns 5 (next largest)
```

### Example: Find K Largest Elements

```java
// import java.util.*;
int[]findKLargest(int[] nums, int k) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>();

    for(int num : nums) {
        maxHeap.push(num);
    }

    int[]result;
    for(int i = 0; i < k && !maxHeap.length == 0; i++) {
        result.add(maxHeap.top());
        maxHeap.pop();
    }

    return result;
}
```

## Custom Comparators

### Using Struct

```java
// Custom comparator for pairs: min heap by second element
class Compare {
    boolean operator()(int[]& a, int[]& b) {
        return a.second > b.second; // Min heap (smaller second element on top)
    }
}
priority_queue<int[], List<int[]>, Compare> pq;

// Example: {value, frequency} - keep element with smallest frequency on top
pq.push({1, 5});
pq.push({2, 3});
pq.push({3, 7});
pq.top(); // Returns {2, 3} (smallest frequency)
```

```java
// Custom class with comparator: min heap by cost
class Node {
    public int cost;
    public int id;
}
class Compare {
    boolean operator()(Node a, Node b) {
        return a.cost > b.cost; // Min heap (smaller cost on top)
    }
}
priority_queue<Node, Node[], Compare> pq;

// Example usage
pq.push({10, 1}); // cost 10, id 1
pq.push({5, 2});  // cost 5, id 2
pq.push({15, 3}); // cost 15, id 3
pq.top(); // Returns {5, 2} (smallest cost)
```

### Using Lambda

```java
// Min heap by distance (for Dijkstra's algorithm)
var distCmp = [](int[]& a, int[]& b) {
    return a.first > b.first; // {distance, node} - min heap by distance
}
priority_queue<int[], List<int[]>, decltype(distCmp)> pq(distCmp);

// Example usage
pq.push({10, 0}); // distance 10 to node 0
pq.push({5, 1});  // distance 5 to node 1
pq.top(); // Returns {5, 1} (smallest distance)
```

### Custom Object Comparator

```java
// Custom object with comparator
class Point {
    public int x, y;
    int dist() { return x x + y y; }
}
class PointCompare {
    boolean operator()(Point a, Point b) {
        return a.dist() > b.dist(); // Min heap by distance
    }
}
priority_queue<Point, Point[], PointCompare> pq;
```

## Common Patterns

### Pattern 1: Maintain K Elements

Keep only K elements in heap, remove smallest/largest when size exceeds K.

```java
// Keep K largest elements
priority_queue<int, int[], greater<int>> minHeap; // Min heap to keep K largest

for(int num : nums) {
    minHeap.push(num);
    if(minHeap.size() > k) {
        minHeap.pop(); // Remove smallest
    }
}
// Now minHeap contains K largest elements
```

### Pattern 2: Frequency-Based

Use heap with frequency counts.

```java
// import java.util.*;
// Top K frequent elements
HashMap<Integer, Integer> freq = new HashMap<Integer, Integer>();
for(int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

priority_queue<int[], List<int[]>, greater<int[]>> minHeap;
// {frequency, element} - min heap by frequency

for(auto& [num, count] : freq) {
    minHeap.push({count, num});
    if(minHeap.size() > k) {
        minHeap.pop();
    }
}
```

## K-way Merge

Merge K sorted lists/arrays using a min heap.

```java
// Merge K sorted lists
ListNode mergeKLists(ListNode[]& lists) {
    var cmp = [](ListNode a, ListNode b) {
        return a.val > b.val; // Min heap by value
    }
    priority_queue<ListNode, ListNode[], decltype(cmp)> pq(cmp);

    // Push first node of each list
    for(ListNode list : lists) {
        if(list) pq.push(list);
    }

    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;

    while(!pq.length == 0) {
        ListNode node = pq.top();
        pq.pop();
        cur.next = node;
        cur = cur.next;
        if(node.next) {
            pq.push(node.next);
        }
    }

    return dummy.next;
}
```

### K-way Merge for Arrays

```java
// Merge K sorted arrays
int[]mergeKSortedArrays(int[][]& arrays) {
    using T = tuple<int, int, int>; // {value, array_index, position}
    priority_queue<T, T[], greater<T>> pq;

    // Push first element of each array
    for(int i = 0; i < arrays.size(); i++) {
        if(!arrays[i].empty()) {
            pq.push({arrays[i][0], i, 0});
        }
    }

    int[]result;
    while(!pq.length == 0) {
        auto [val, arrIdx, pos] = pq.top();
        pq.pop();
        result.add(val);

        if(pos + 1 < arrays[arrIdx].size()) {
            pq.push({arrays[arrIdx][pos + 1], arrIdx, pos + 1});
        }
    }

    return result;
}
```

## Top K Elements

### Top K Frequent Elements

```java
// import java.util.*;
int[]topKFrequent(int[] nums, int k) {
    HashMap<Integer, Integer> freq = new HashMap<Integer, Integer>();
    for(int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

    // Min heap: {frequency, element}
    priority_queue<int[], List<int[]>, greater<int[]>> minHeap;

    for(auto& [num, count] : freq) {
        minHeap.push({count, num});
        if(minHeap.size() > k) {
            minHeap.pop(); // Remove element with smallest frequency
        }
    }

    int[]result;
    while(!minHeap.length == 0) {
        result.add(minHeap.top().second);
        minHeap.pop();
    }

    return result;
}
```

### K Closest Points to Origin

```java
int[][] kClosest(int[][]& points, int k) {
    var distCmp = [](int[] a, int[] b) {
        int distA = a[0]*a[0] + a[1]*a[1];
        int distB = b[0]*b[0] + b[1]*b[1];
        return distA < distB; // Max heap (larger distance on top)
    }
    priority_queue<int[], int[][], decltype(distCmp)> maxHeap(distCmp);

    for(auto point : points) {
        maxHeap.push(point);
        if(maxHeap.size() > k) {
            maxHeap.pop(); // Remove point with largest distance
        }
    }

    int[][] result;
    while(!maxHeap.length == 0) {
        result.add(maxHeap.top());
        maxHeap.pop();
    }

    return result;
}
```

### Kth Largest Element in an Array (LC 215)

**Solution 1: Min Heap (O(n log k))**

Keep a min heap of size k. The top element will be the kth largest.

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        priority_queue<int, int[], greater<>> minHeap;
        for(int num: nums) {
            minHeap.push(num);
            if(minHeap.size() > k) minHeap.pop();
        }
        return minHeap.top();
    }
}
```

**Solution 2: QuickSelect (O(n) average, O(n²) worst case)**

Use partition-based selection algorithm.

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        int N = nums.length;
        return quickSelect(nums, 0, N - 1, N - k);
    }
    int quickSelect(int[] nums, int l, int r, int k) {
        if(l == r) return nums[k];
        int pivot = nums[l], i = l - 1, j = r + 1;
        while(i < j) {
            do i++; while(nums[i] < pivot);
            do j--; while(nums[j] > pivot);
            if(i < j)
                swap(nums[i], nums[j]);
        }
        if(k <= j) return quickSelect(nums, l, j, k);
        else return quickSelect(nums, j + 1, r, k);
    }
}
```

**Comparison:**
- **Heap**: O(n log k) time, O(k) space - Simple and efficient for small k
- **QuickSelect**: O(n) average time, O(n²) worst case, O(1) space - Better for large k

## Two Heaps

Maintain two heaps to find median or balance elements.

### Find Median from Data Stream

```java
// import java.util.*;
class MedianFinder {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>(); // Lower half (max heap)
    priority_queue<int, int[], greater<int>> minHeap; // Upper half (min heap)
    void addNum(int num) {
        maxHeap.push(num);
        minHeap.push(maxHeap.top());
        maxHeap.pop();

        if(maxHeap.size() < minHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }

    double findMedian() {
        if(maxHeap.size() > minHeap.size()) {
            return maxHeap.top();
        }
        return (maxHeap.top() + minHeap.top()) / 2.0;
    }
}
```

### Sliding Window Median

```java
double[]medianSlidingWindow(int[] nums, int k) {
    multiset<int> window(nums.iterator(), nums.iterator() + k);
    var mid = next(window.iterator(), k / 2);
    double[]medians;

    for(int i = k; i <= nums.length; i++) {
        medians.add((double(*mid) + *prev(mid, 1 - k % 2)) / 2.0);

        if(i == nums.length) break;

        window.add(nums[i]);
        if(nums[i] < *mid) mid--;
        if(nums[i - k] <= *mid) mid++;
        window.remove(window.binary search (lower bound)(nums[i - k]));
    }

    return medians;
}
```

## Dijkstra's Algorithm

Use min heap for shortest path finding.

```java
// Shortest path from source to all nodes
int[]dijkstra(vector<List<int[]>>& graph, int start) {
    int n = graph.size();
    int[]dist(n, Integer.MAX_VALUE);
    dist[start] = 0;

    // Min heap: {distance, node}
    var cmp = [](int[]& a, int[]& b) {
        return a.first > b.first; // Min heap by distance
    }
    priority_queue<int[], List<int[]>, decltype(cmp)> pq(cmp);
    pq.push({0, start});

    while(!pq.length == 0) {
        auto [d, u] = pq.top();
        pq.pop();

        if(d > dist[u]) continue; // Already processed with better distance

        for(auto& [v, weight] : graph[u]) {
            int newDist = dist[u] + weight;
            if(newDist < dist[v]) {
                dist[v] = newDist;
                pq.push({newDist, v});
            }
        }
    }

    return dist;
}
```

## Easy Problems

| ID | Title | Link | Solution |
|---|---|---|---|
| 703 | Kth Largest Element in a Stream | [Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | - |
| 1046 | Last Stone Weight | [Link](https://leetcode.com/problems/last-stone-weight/) | - |
| 1167 | Minimum Cost to Connect Sticks | [Link](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) | - |

## Medium Problems

| ID | Title | Link | Solution |
|---|---|---|---|
| 23 | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/02/15/hard-23-merge-k-sorted-lists/) |
| 215 | Kth Largest Element in an Array | [Link](https://leetcode.com/problems/kth-largest-element-in-an-array/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/05/medium-215-kth-largest-element-in-an-array/) |
| 253 | Meeting Rooms II | [Link](https://leetcode.com/problems/meeting-rooms-ii/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-11-medium-253-meeting-rooms-ii/) |
| 295 | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) | - |
| 347 | Top K Frequent Elements | [Link](https://leetcode.com/problems/top-k-frequent-elements/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-21-medium-347-top-k-frequent-elements/) |
| 378 | Kth Smallest Element in a Sorted Matrix | [Link](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | - |
| 692 | Top K Frequent Words | [Link](https://leetcode.com/problems/top-k-frequent-words/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/08/medium-692-top-k-frequent-words/) |
| 621 | Task Scheduler | [Link](https://leetcode.com/problems/task-scheduler/) | - |
| 767 | Reorganize String | [Link](https://leetcode.com/problems/reorganize-string/) | - |
| 973 | K Closest Points to Origin | [Link](https://leetcode.com/problems/k-closest-points-to-origin/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-21-medium-973-k-closest-points-to-origin/) |
| 1976 | Number of Ways to Arrive at Destination | [Link](https://leetcode.com/problems/number-of-ways-to-arrive-at-destination/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2025/12/28/medium-1976-number-of-ways-to-arrive-at-destination/) |
| 2406 | Divide Intervals Into Minimum Number of Groups | [Link](https://leetcode.com/problems/divide-intervals-into-minimum-number-of-groups/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/03/16/medium-2406-divide-intervals-into-minimum-number-of-groups/) |
| 1353 | Maximum Number of Events That Can Be Attended | [Link](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/04/13/medium-1353-maximum-number-of-events-that-can-be-attended/) |

## Hard Problems

| ID | Title | Link | Solution |
|---|---|---|---|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-239-sliding-window-maximum/) |
| 480 | Sliding Window Median | [Link](https://leetcode.com/problems/sliding-window-median/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-480-sliding-window-median/) |
| 743 | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) | - |
| 787 | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | - |
| 871 | Minimum Number of Refueling Stops | [Link](https://leetcode.com/problems/minimum-number-of-refueling-stops/) | - |

## Common Heap Patterns

### Pattern 1: K Largest/Smallest
- Use min heap to keep K largest (remove smallest when size > K)
- Use max heap to keep K smallest (remove largest when size > K)

### Pattern 2: Frequency-Based
- Count frequencies, use heap to find top K by frequency

### Pattern 3: K-way Merge
- Push first element of each sequence into min heap
- Pop smallest, push next element from same sequence

### Pattern 4: Two Heaps
- Maintain two balanced heaps for median finding
- One heap for lower half, one for upper half

### Pattern 5: Shortest Path
- Use min heap in Dijkstra's algorithm
- Store {distance, node} pairs

## Key Insights

1. **Min Heap for K Largest**: Keep K largest by removing smallest
2. **Max Heap for K Smallest**: Keep K smallest by removing largest
3. **Custom Comparators**: Use lambda or struct for complex ordering
4. **Two Heaps**: Balance two heaps for median problems
5. **Efficiency**: Heap operations are O(log n), making it efficient for dynamic problems

## Time Complexity

| Operation | Time Complexity |
|-----------|----------------|
| `push()` | O(log n) |
| `pop()` | O(log n) |
| `top()` | O(1) |
| `empty()` | O(1) |
| `size()` | O(1) |

## Space Complexity

- **Heap Storage**: O(n) where n is number of elements
- **Auxiliary Space**: O(1) for operations (excluding storage)

## When to Use Heap

1. **K Largest/Smallest**: Finding top K elements
2. **K-way Merge**: Merging K sorted sequences
3. **Scheduling**: Meeting rooms, task scheduling
4. **Shortest Path**: Dijkstra's algorithm
5. **Median Finding**: Two heaps pattern
6. **Frequency Problems**: Top K frequent elements

## Common Mistakes

1. **Wrong Comparator**: Using `>` instead of `<` (or vice versa) for min/max heap
2. **Not Handling Empty**: Accessing `top()` without checking `empty()`
3. **Wrong Heap Type**: Using max heap when min heap is needed
4. **Not Maintaining Size**: Forgetting to pop when size exceeds K
5. **Custom Comparator Logic**: Reversing the comparison logic incorrectly

## Related Data Structures

- **Set/Multiset**: For maintaining sorted order with duplicates
- **Map**: For frequency counting before heap operations
- **Deque**: For sliding window problems (alternative to heap)

## More templates

- **Data structures (heap, monotonic queue):** [Data Structures & Core Algorithms](/posts/2025-10-29-leetcode-templates-data-structures/)
- **Graph (Dijkstra):** [Graph](/posts/2025-10-29-leetcode-templates-graph/)
- **Master index:** [Categories & Templates](/posts/2025-10-29-leetcode-categories-and-templates/)

{% endraw %}

