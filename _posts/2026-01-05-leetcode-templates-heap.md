---
layout: post
title: "Algorithm Templates: Heap"
date: 2026-01-05 00:00:00 -0700
categories: leetcode templates heap priority-queue
permalink: /posts/2026-01-05-leetcode-templates-heap/
tags: [leetcode, templates, heap, priority-queue, data-structures]
---

{% raw %}
Minimal, copy-paste Java for min/max heap, K-way merge, top K, and two heaps. See also [Data Structures](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/) for heap patterns.

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
// Min heap (smallest element at top)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// Basic operations
minHeap.offer(5);
minHeap.offer(2);
minHeap.offer(8);
minHeap.offer(1);

minHeap.peek();    // Returns 1 (smallest)
minHeap.poll();    // Removes 1
minHeap.peek();    // Returns 2 (next smallest)
```

### Example: Find K Smallest Elements

```java
int[] findKSmallest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) minHeap.offer(num);
    int[] result = new int[k];
    for (int i = 0; i < k && !minHeap.isEmpty(); i++) {
        result[i] = minHeap.poll();
    }
    return result;
}
```

## Max Heap

Max heap keeps the largest element at the top (default in C++; use `Comparator.reverseOrder()` in Java).

```java
// Max heap (largest element at top)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

maxHeap.offer(5);
maxHeap.offer(2);
maxHeap.offer(8);
maxHeap.offer(1);

maxHeap.peek();    // Returns 8 (largest)
maxHeap.poll();    // Removes 8
maxHeap.peek();    // Returns 5 (next largest)
```

### Example: Find K Largest Elements

```java
int[] findKLargest(int[] nums, int k) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    for (int num : nums) maxHeap.offer(num);
    int[] result = new int[k];
    for (int i = 0; i < k && !maxHeap.isEmpty(); i++) {
        result[i] = maxHeap.poll();
    }
    return result;
}
```

## Custom Comparators

### Pair Comparator

```java
// Min heap by second element (frequency)
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[] {1, 5});
pq.offer(new int[] {2, 3});
pq.offer(new int[] {3, 7});
pq.peek(); // {2, 3}
```

### Custom Object Comparator

```java
record Node(int cost, int id) {}
PriorityQueue<Node> pq = new PriorityQueue<>(Comparator.comparingInt(n -> n.cost));
pq.offer(new Node(10, 1));
pq.offer(new Node(5, 2));
pq.peek(); // Node(5, 2)
```

### Distance Comparator (Dijkstra)

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
pq.offer(new int[] {10, 0});
pq.offer(new int[] {5, 1});
pq.peek(); // {5, 1}
```

### Point Comparator

```java
record Point(int x, int y) {
    int distSq() { return x * x + y * y; }
}
PriorityQueue<Point> pq = new PriorityQueue<>(Comparator.comparingInt(Point::distSq));
```

## Common Patterns

### Pattern 1: Maintain K Elements

```java
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll();
}
```

### Pattern 2: Frequency-Based

```java
Map<Integer, Integer> freq = new HashMap<>();
for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
for (var e : freq.entrySet()) {
    minHeap.offer(new int[] {e.getValue(), e.getKey()});
    if (minHeap.size() > k) minHeap.poll();
}
```

## K-way Merge

```java
ListNode mergeKLists(ListNode[] lists) {
    PriorityQueue<ListNode> pq = new PriorityQueue<>(Comparator.comparingInt(n -> n.val));
    for (ListNode head : lists) if (head != null) pq.offer(head);
    ListNode dummy = new ListNode(0), cur = dummy;
    while (!pq.isEmpty()) {
        ListNode node = pq.poll();
        cur.next = node;
        cur = cur.next;
        if (node.next != null) pq.offer(node.next);
    }
    return dummy.next;
}
```

### K-way Merge for Arrays

```java
int[] mergeKSortedArrays(int[][] arrays) {
    record Entry(int val, int arrIdx, int pos) {}
    PriorityQueue<Entry> pq = new PriorityQueue<>(Comparator.comparingInt(e -> e.val));
    for (int i = 0; i < arrays.length; i++) {
        if (arrays[i].length > 0) pq.offer(new Entry(arrays[i][0], i, 0));
    }
    List<Integer> result = new ArrayList<>();
    while (!pq.isEmpty()) {
        Entry e = pq.poll();
        result.add(e.val);
        int next = e.pos + 1;
        if (next < arrays[e.arrIdx].length) {
            pq.offer(new Entry(arrays[e.arrIdx][next], e.arrIdx, next));
        }
    }
    return result.stream().mapToInt(Integer::intValue).toArray();
}
```

## Top K Elements

### Top K Frequent Elements

```java
int[] topKFrequent(int[] nums, int k) {
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
```

### K Closest Points to Origin

```java
int[][] kClosest(int[][] points, int k) {
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> {
        int da = a[0] * a[0] + a[1] * a[1];
        int db = b[0] * b[0] + b[1] * b[1];
        return Integer.compare(db, da);
    });
    for (int[] p : points) {
        maxHeap.offer(p);
        if (maxHeap.size() > k) maxHeap.poll();
    }
    int[][] result = new int[k][2];
    for (int i = k - 1; i >= 0; i--) result[i] = maxHeap.poll();
    return result;
}
```

### Kth Largest Element in an Array (LC 215)

**Solution 1: Min Heap (O(n log k))**

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }
        return minHeap.peek();
    }
}
```

**Solution 2: QuickSelect (O(n) average)**

```java
class Solution {
    public int findKthLargest(int[] nums, int k) {
        return quickSelect = new return(nums, 0, nums.length - 1, nums.length - k);
    }

    private int quickSelect(int[] nums, int l, int r, int k) {
        if (l == r) return nums[k];
        int pivot = nums[l], i = l - 1, j = r + 1;
        while (i < j) {
            while (nums[++i] < pivot);
            while (nums[--j] > pivot);
            if (i < j) { int t = nums[i]; nums[i] = nums[j]; nums[j] = t; }
        }
        if (k <= j) return quickSelect = new return(nums, l, j, k);
        return quickSelect = new return(nums, j + 1, r, k);
    }
}
```

## Two Heaps

### Find Median from Data Stream

```java
class MedianFinder {
    private final PriorityQueue<Integer> lo = new PriorityQueue<>(Comparator.reverseOrder());
    private final PriorityQueue<Integer> hi = new PriorityQueue<>();

    public void addNum(int num) {
        lo.offer(num);
        hi.offer(lo.poll());
        if (lo.size() < hi.size()) lo.offer(hi.poll());
    }

    public double findMedian() {
        return lo.size() > hi.size() ? lo.peek() : (lo.peek() + hi.peek()) / 2.0;
    }
}
```

### Sliding Window Median

```java
// Sliding window median (LC 480) typically uses two balanced heaps
// or a TreeMultiset-style structure. See the dedicated LC 480 post for a full solution.
```

## Dijkstra's Algorithm

```java
int[] dijkstra(List<List<int[]>> graph, int start) {
    int n = graph.size();
    int[] dist = new int[n];
    Arrays.fill(dist, Integer.MAX_VALUE);
    dist[start] = 0;
    PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
    pq.offer(new int[] {0, start});
    while (!pq.isEmpty()) {
        int[] cur = pq.poll();
        int d = cur[0], u = cur[1];
        if (d > dist[u]) continue;
        for (int[] e : graph.get(u)) {
            int v = e[0], w = e[1];
            if (dist[u] + w < dist[v]) {
                dist[v] = dist[u] + w;
                pq.offer(new int[] {dist[v], v});
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

- **Data structures (heap, monotonic queue):** [Data Structures & Core Algorithms](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-data-structures/)
- **Graph (Dijkstra):** [Graph](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/)
- **Master index:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)

{% endraw %}

