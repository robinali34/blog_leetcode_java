---
layout: post
title: "Algorithm Templates: Heap"
date: 2026-01-05 00:00:00 -0700
categories: leetcode templates heap priority-queue
permalink: /posts/2026-01-05-leetcode-templates-heap/
tags: [leetcode, templates, heap, priority-queue, data-structures]
---
{% raw %}
Welcome to the Heap templates page! Here you'll find battle-tested Java snippets for every common heap (priority queue) pattern on LeetCode — from basic min/max heaps to advanced techniques like K-way merge, Two Heaps for medians, and Dijkstra's shortest path. Each section is self-contained so you can copy-paste directly into your solutions. See also [Data Structures](/posts/2025-10-29-leetcode-templates-data-structures/) for related patterns.

> **New to Heaps?** A heap (priority queue) always gives you the smallest (min-heap) or largest (max-heap) element in O(1). Think of it as a self-sorting container. Whenever a problem says "k largest", "k smallest", "median", or "merge sorted lists", think heap.
## Summary Table
| Pattern | Signal Phrases | Key Idea |
|---|---|---|
| Min Heap | "k largest", "sort" | Keep smallest on top |
| Max Heap | "k smallest" | Keep largest on top |
| K-way Merge | "merge k sorted" | Push heads, pop smallest |
| Top K | "kth largest", "top k frequent" | Heap of size k |
| Two Heaps | "median", "sliding median" | Max-heap for lower half, min-heap for upper |
| Dijkstra | "shortest path", "minimum cost" | Greedy + min-heap |

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

In Java, `PriorityQueue` is a min-heap by default. To get a min-heap, use the default constructor for a min-heap, or pass `Comparator.reverseOrder()` for max-heap as the comparator.

**Key Operations:**

| Operation | What it does | Time |
|-----------|-------------|------|
| `offer(x)` | Insert element | O(log n) |
| `poll()` | Remove top element | O(log n) |
| `peek()` | Access top element (min or max) | O(1) |
| `isEmpty()` | Check if empty | O(1) |
| `size()` | Get number of elements | O(1) |

**Use Cases:**
- Finding K largest/smallest elements
- Merging K sorted sequences
- Maintaining running median
- Shortest path algorithms (Dijkstra's)
- Scheduling problems (meeting rooms, task ordering)
- Stream processing (continuously arriving data)

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 305" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <text x="350" y="18" text-anchor="middle" font-size="14" font-weight="600" fill="#3A3530">Min-Heap: Tree Structure and Array Representation</text>
  <!-- Tree edges -->
  <line x1="350" y1="60" x2="210" y2="105" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="350" y1="60" x2="490" y2="105" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="210" y1="135" x2="140" y2="178" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="210" y1="135" x2="280" y2="178" stroke="#B8B5B0" stroke-width="1.5"/>
  <line x1="490" y1="135" x2="420" y2="178" stroke="#B8B5B0" stroke-width="1.5"/>
  <!-- Tree nodes with index annotations -->
  <circle cx="350" cy="48" r="20" fill="#D4D8D0" stroke="#8B9B86" stroke-width="2"/>
  <text x="350" y="53" text-anchor="middle" font-size="15" font-weight="700" fill="#3A3530">1</text>
  <text x="374" y="37" font-size="9" fill="#9A9792">i=0</text>
  <circle cx="210" cy="120" r="18" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="210" y="125" text-anchor="middle" font-size="14" font-weight="600" fill="#3A3530">3</text>
  <text x="232" y="109" font-size="9" fill="#9A9792">i=1</text>
  <circle cx="490" cy="120" r="18" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="490" y="125" text-anchor="middle" font-size="14" font-weight="600" fill="#3A3530">5</text>
  <text x="512" y="109" font-size="9" fill="#9A9792">i=2</text>
  <circle cx="140" cy="188" r="16" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="140" y="193" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">7</text>
  <text x="160" y="178" font-size="9" fill="#9A9792">i=3</text>
  <circle cx="280" cy="188" r="16" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="280" y="193" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">9</text>
  <text x="300" y="178" font-size="9" fill="#9A9792">i=4</text>
  <circle cx="420" cy="188" r="16" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="420" y="193" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">8</text>
  <text x="440" y="178" font-size="9" fill="#9A9792">i=5</text>
  <!-- Array representation -->
  <text x="350" y="228" text-anchor="middle" font-size="11" font-weight="600" fill="#5A5752">Array: stored level-by-level, left to right</text>
  <rect x="155" y="236" width="48" height="28" rx="4" fill="#D4D8D0" stroke="#8B9B86" stroke-width="1.5"/>
  <text x="179" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">1</text>
  <rect x="203" y="236" width="48" height="28" rx="4" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="227" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">3</text>
  <rect x="251" y="236" width="48" height="28" rx="4" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="275" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">5</text>
  <rect x="299" y="236" width="48" height="28" rx="4" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="323" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">7</text>
  <rect x="347" y="236" width="48" height="28" rx="4" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="371" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">9</text>
  <rect x="395" y="236" width="48" height="28" rx="4" fill="#E8D5D0" stroke="#B8A5A0" stroke-width="1.5"/>
  <text x="419" y="254" text-anchor="middle" font-size="13" font-weight="600" fill="#3A3530">8</text>
  <!-- Array index labels -->
  <text x="179" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[0]</text>
  <text x="227" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[1]</text>
  <text x="275" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[2]</text>
  <text x="323" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[3]</text>
  <text x="371" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[4]</text>
  <text x="419" y="278" text-anchor="middle" font-size="9" fill="#9A9792">[5]</text>
  <!-- Relationship formulas -->
  <text x="350" y="300" text-anchor="middle" font-size="10" fill="#7A7772">parent = (i-1)/2 · left child = 2i+1 · right child = 2i+2 · parent ≤ children everywhere</text>
</svg>

### How a Min-Heap Works (Visualization)

<svg viewBox="0 0 400 280" xmlns="http://www.w3.org/2000/svg" style="max-width:400px;font-family:monospace">
  <!-- Edges -->
  <line x1="200" y1="38" x2="120" y2="98" stroke="#b8a9c9" stroke-width="2"/>
  <line x1="200" y1="38" x2="280" y2="98" stroke="#b8a9c9" stroke-width="2"/>
  <line x1="120" y1="98" x2="80" y2="158" stroke="#b8a9c9" stroke-width="2"/>
  <line x1="120" y1="98" x2="160" y2="158" stroke="#b8a9c9" stroke-width="2"/>
  <line x1="280" y1="98" x2="240" y2="158" stroke="#b8a9c9" stroke-width="2"/>
  <!-- Nodes -->
  <circle cx="200" cy="35" r="20" fill="#a3b18a" stroke="#588157" stroke-width="2"/>
  <text x="200" y="40" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">1</text>
  <circle cx="120" cy="95" r="20" fill="#dda15e" stroke="#bc6c25" stroke-width="2"/>
  <text x="120" y="100" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">3</text>
  <circle cx="280" cy="95" r="20" fill="#dda15e" stroke="#bc6c25" stroke-width="2"/>
  <text x="280" y="100" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">2</text>
  <circle cx="80" cy="155" r="20" fill="#e9c46a" stroke="#c9a227" stroke-width="2"/>
  <text x="80" y="160" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">7</text>
  <circle cx="160" cy="155" r="20" fill="#e9c46a" stroke="#c9a227" stroke-width="2"/>
  <text x="160" y="160" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">4</text>
  <circle cx="240" cy="155" r="20" fill="#e9c46a" stroke="#c9a227" stroke-width="2"/>
  <text x="240" y="160" text-anchor="middle" fill="#fff" font-size="14" font-weight="bold">5</text>
  <!-- Labels -->
  <text x="200" y="210" text-anchor="middle" fill="#6b705c" font-size="12">Array: [1, 3, 2, 7, 4, 5]</text>
  <text x="200" y="230" text-anchor="middle" fill="#6b705c" font-size="11">push(x): add to end, bubble UP to maintain order</text>
  <text x="200" y="248" text-anchor="middle" fill="#6b705c" font-size="11">pop(): remove root (min), move last to root, bubble DOWN</text>
  <text x="200" y="266" text-anchor="middle" fill="#6b705c" font-size="11">top(): always returns root = smallest element → O(1)</text>
</svg>

## Min Heap
**When to use:** You need the smallest element quickly — "k largest elements" (use min-heap of size k), sorting streams, or Dijkstra's algorithm.

Min heap keeps the smallest element at the top.



### Example: Find K Smallest Elements

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
**When to use:** You need the largest element quickly — "k smallest elements" (use max-heap of size k), greedy scheduling, or "last stone weight" style problems.

Max heap keeps the largest element at the top (default in C++).



### Example: Find K Largest Elements

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
**When to use:** The heap elements are structs, pairs, or tuples and you need to order by a specific field (e.g., sort by cost, frequency, or distance).

### Using Struct





### Using Lambda



### Custom Object Comparator

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

Keep only K elements in heap, remove smallest/largest when size exceeds K.



### Pattern 2: Frequency-Based

Use heap with frequency counts.

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
**When to use:** The problem says "merge k sorted lists/arrays" or you need to produce a globally sorted sequence from multiple sorted sources.

Merge K sorted lists/arrays using a min heap.



### K-way Merge for Arrays

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
**When to use:** The problem asks for "kth largest", "top k frequent", "k closest" — maintain a heap of size k and evict the least relevant element.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 250" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#8B8680"/></marker>
    <marker id="ahg" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#8B9B86"/></marker>
    <marker id="ahr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#B8A5A0"/></marker>
  </defs>
  <text x="360" y="20" text-anchor="middle" font-size="14" font-weight="600" fill="#3A3530">Top-K Pattern: Min-Heap of Size K Filters the K Largest</text>
  <!-- Input stream -->
  <text x="25" y="60" font-size="11" font-weight="600" fill="#5A5752">Input stream</text>
  <rect x="15" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="30" y="86" text-anchor="middle" font-size="11" fill="#3A3530">4</text>
  <rect x="49" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="64" y="86" text-anchor="middle" font-size="11" fill="#3A3530">7</text>
  <rect x="83" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="98" y="86" text-anchor="middle" font-size="11" fill="#3A3530">2</text>
  <rect x="117" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="132" y="86" text-anchor="middle" font-size="11" fill="#3A3530">9</text>
  <rect x="151" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="166" y="86" text-anchor="middle" font-size="11" fill="#3A3530">1</text>
  <rect x="185" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="200" y="86" text-anchor="middle" font-size="11" fill="#3A3530">5</text>
  <rect x="219" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="234" y="86" text-anchor="middle" font-size="11" fill="#3A3530">8</text>
  <rect x="253" y="70" width="30" height="24" rx="4" fill="#E8E3D8" stroke="#B8B5B0" stroke-width="1"/>
  <text x="268" y="86" text-anchor="middle" font-size="11" fill="#3A3530">3</text>
  <!-- Arrow to heap -->
  <line x1="290" y1="82" x2="348" y2="82" stroke="#8B8680" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- Heap container -->
  <rect x="358" y="38" width="180" height="130" rx="10" fill="#FAF8F5" stroke="#B8B5B0" stroke-width="1.5"/>
  <text x="448" y="56" text-anchor="middle" font-size="11" font-weight="600" fill="#5A5752">Min-Heap (K = 3)</text>
  <!-- Heap tree inside -->
  <line x1="448" y1="80" x2="412" y2="108" stroke="#B8B5B0" stroke-width="1.2"/>
  <line x1="448" y1="80" x2="484" y2="108" stroke="#B8B5B0" stroke-width="1.2"/>
  <circle cx="448" cy="74" r="14" fill="#D4D8D0" stroke="#8B9B86" stroke-width="1.5"/>
  <text x="448" y="78" text-anchor="middle" font-size="12" font-weight="600" fill="#3A3530">7</text>
  <circle cx="412" cy="114" r="14" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="412" y="118" text-anchor="middle" font-size="12" font-weight="600" fill="#3A3530">8</text>
  <circle cx="484" cy="114" r="14" fill="#D4D8E0" stroke="#8B8680" stroke-width="1.5"/>
  <text x="484" y="118" text-anchor="middle" font-size="12" font-weight="600" fill="#3A3530">9</text>
  <text x="448" y="152" text-anchor="middle" font-size="9" fill="#7A7772">top() = smallest kept</text>
  <!-- Arrow to result -->
  <line x1="543" y1="82" x2="598" y2="82" stroke="#8B9B86" stroke-width="1.5" marker-end="url(#ahg)"/>
  <!-- Result box -->
  <rect x="608" y="56" width="100" height="56" rx="8" fill="#C8D5C4" stroke="#8B9B86" stroke-width="1.5"/>
  <text x="658" y="76" text-anchor="middle" font-size="11" font-weight="600" fill="#3A3530">Top-3</text>
  <text x="658" y="94" text-anchor="middle" font-size="12" fill="#3A3530">{7, 8, 9}</text>
  <text x="658" y="108" text-anchor="middle" font-size="9" fill="#7A7772">K largest</text>
  <!-- Eviction arrow -->
  <line x1="448" y1="170" x2="448" y2="200" stroke="#B8A5A0" stroke-width="1.5" marker-end="url(#ahr)"/>
  <!-- Evicted info -->
  <text x="448" y="220" text-anchor="middle" font-size="11" fill="#B8A5A0">Evicted: 1, 2, 3, 4, 5</text>
  <text x="448" y="238" text-anchor="middle" font-size="10" fill="#9A9792">new &gt; top() → push new, pop smallest</text>
</svg>

### Top K Frequent Elements



### K Closest Points to Origin



### Kth Largest Element in an Array (LC 215)

**Solution 1: Min Heap (O(n log k))**

Keep a min heap of size k. The top element will be the kth largest.



**Solution 2: QuickSelect (O(n) average, O(n²) worst case)**

Use partition-based selection algorithm.



**Comparison:**
- **Heap**: O(n log k) time, O(k) space - Simple and efficient for small k
- **QuickSelect**: O(n) average time, O(n²) worst case, O(1) space - Better for large k

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
**When to use:** The problem mentions "median", "sliding median", or requires tracking the middle value of a dynamic stream. Use a max-heap for the lower half and a min-heap for the upper half.

Maintain two heaps to find median or balance elements.

### Find Median from Data Stream



### Sliding Window Median

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
**When to use:** The problem asks for "shortest path", "minimum cost path", or "cheapest route" in a weighted graph with non-negative edges.

Use min heap for shortest path finding.

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
| `poll()` | O(log n) |
| `peek()` | O(1) |
| `isEmpty()` | O(1) |
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
2. **Not Handling Empty**: Accessing `peek()` without checking `isEmpty()`
3. **Wrong Heap Type**: Using max heap when min heap is needed
4. **Not Maintaining Size**: Forgetting to pop when size exceeds K
5. **Custom Comparator Logic**: Reversing the comparison logic incorrectly

## Related Data Structures
- **Set/Multiset**: For maintaining sorted order with duplicates
- **Map**: For frequency counting before heap operations
- **Deque**: For sliding window problems (alternative to heap)

## More templates
- **Beginner's Guide:** [LeetCode Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/)
- **Data structures (heap, monotonic queue):** [Data Structures & Core Algorithms](/posts/2025-10-29-leetcode-templates-data-structures/)
- **Graph (Dijkstra):** [Graph](/posts/2025-10-29-leetcode-templates-graph/)
- **Master index:** [Categories & Templates](/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}
