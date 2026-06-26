---
layout: post
title: "Algorithm Templates: Queue"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates queue
permalink: /posts/2025-11-24-leetcode-templates-queue/
tags: [leetcode, templates, queue, data-structures]
---
{% raw %}
Queues are one of the most versatile data structures in algorithm problems. This page collects ready-to-use Java templates for every queue variant you'll encounter on LeetCode — from the basic FIFO queue used in BFS to monotonic queues, priority queues, and deques. Each section includes the template code and a curated problem list so you can practice immediately.

See also [Graph](/posts/2025-10-29-leetcode-templates-graph/) and [Data Structures](/posts/2025-10-29-leetcode-templates-data-structures/) (monotonic queue).

> **Queue = First-In-First-Out (FIFO).** Use a queue whenever you need to process elements in the order they arrived — most commonly in BFS. A deque (double-ended queue) lets you push/pop from both ends.

- **Beginner's Guide:** [LeetCode Beginner's Guide](/blog_leetcode_java/posts/2026-06-25-leetcode-beginners-guide/)

<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
  <text x="180" y="20" font-size="12" fill="#5A5752" font-weight="700" text-anchor="middle">Queue (FIFO)</text>
  <rect x="30" y="35" width="300" height="50" rx="8" fill="#FAF8F5" stroke="#D4D1CC"/>
  <text x="50" y="55" font-size="10" fill="#9A9792">front →</text>
  <rect x="100" y="45" width="50" height="30" rx="4" fill="#D4D8E0" stroke="#B8B5B0"/><text x="125" y="64" font-size="12" fill="#5A5752" text-anchor="middle">1</text>
  <rect x="155" y="45" width="50" height="30" rx="4" fill="#D4D8D0" stroke="#B8B5B0"/><text x="180" y="64" font-size="12" fill="#5A5752" text-anchor="middle">2</text>
  <rect x="200" y="45" width="50" height="30" rx="4" fill="#E8D5D0" stroke="#B8B5B0"/><text x="225" y="64" font-size="12" fill="#5A5752" text-anchor="middle">3</text>
  <text x="260" y="55" font-size="10" fill="#9A9792">← back</text>
  <text x="180" y="95" font-size="10" fill="#5A5752" text-anchor="middle">push → back | pop → front | BFS uses queue</text>
  <text x="540" y="20" font-size="12" fill="#5A5752" font-weight="700" text-anchor="middle">Deque (both ends)</text>
  <rect x="400" y="35" width="300" height="50" rx="8" fill="#FAF8F5" stroke="#D4D1CC"/>
  <text x="420" y="55" font-size="10" fill="#9A9792">front →</text>
  <rect x="470" y="45" width="50" height="30" rx="4" fill="#E8E3D8" stroke="#B8B5B0"/><text x="495" y="64" font-size="12" fill="#5A5752" text-anchor="middle">5</text>
  <rect x="525" y="45" width="50" height="30" rx="4" fill="#D4D8E0" stroke="#B8B5B0"/><text x="550" y="64" font-size="12" fill="#5A5752" text-anchor="middle">3</text>
  <rect x="580" y="45" width="50" height="30" rx="4" fill="#D4D8D0" stroke="#B8B5B0"/><text x="605" y="64" font-size="12" fill="#5A5752" text-anchor="middle">1</text>
  <text x="660" y="55" font-size="10" fill="#9A9792">← back</text>
  <text x="540" y="95" font-size="10" fill="#5A5752" text-anchor="middle">push_front / push_back | sliding window, 0-1 BFS</text>
  <text x="360" y="130" font-size="12" fill="#5A5752" font-weight="700" text-anchor="middle">Monotonic Queue — sliding window max for [1,3,-1,-3,5,3,6,7], k=3</text>
  <rect x="120" y="145" width="480" height="30" rx="4" fill="#F0EBE6" stroke="#D4D1CC"/>
  <text x="140" y="165" font-size="11" fill="#5A5752">1</text><text x="200" y="165" font-size="11" fill="#5A5752">3</text><text x="260" y="165" font-size="11" fill="#5A5752">-1</text><text x="320" y="165" font-size="11" fill="#5A5752">-3</text><text x="380" y="165" font-size="11" fill="#5A5752">5</text><text x="440" y="165" font-size="11" fill="#5A5752">3</text><text x="500" y="165" font-size="11" fill="#5A5752">6</text><text x="560" y="165" font-size="11" fill="#5A5752">7</text>
  <text x="360" y="200" font-size="10" fill="#5A5752" text-anchor="middle">Deque keeps indices in decreasing order → front always has window maximum</text>
  <text x="360" y="215" font-size="10" fill="#3A6B3A" font-weight="600" text-anchor="middle">Output: [3, 3, 5, 5, 6, 7]</text>
</svg>
## Summary
| Pattern | Signal Phrases | Key Idea |
|---|---|---|
| BFS Queue | "shortest path", "level order" | Process nodes level by level |
| Monotonic Queue | "sliding window max/min" | Maintain decreasing/increasing order |
| Priority Queue | "k-th largest", "merge k sorted" | Auto-sorted by priority |
| Circular Queue | "circular buffer", "design queue" | Wrap-around with modulo |
| Deque | "sliding window", "both ends" | Push/pop from front and back |

## Contents
- [Basic Queue Operations](#basic-queue-operations)
- [BFS with Queue](#bfs-with-queue)
- [Monotonic Queue](#monotonic-queue)
- [Priority Queue](#priority-queue)
- [Circular Queue](#circular-queue)
- [Double-ended Queue (Deque)](#double-ended-queue-deque)

## Basic Queue Operations
**When to use:** any problem requiring FIFO ordering, or when implementing a queue from scratch (e.g., using two stacks).



### Implement Queue using Stacks



| ID | Title | Link | Solution |
|---|---|---|---|
| 232 | Implement Queue using Stacks | [Link](https://leetcode.com/problems/implement-queue-using-stacks/) | - |

```java
// import java.util.*;

// Standard queue operations
Queue<Integer> q = new LinkedList<>();
q.offer(1);        // Enqueue
q.get(0);        // Peek front
q.get(q.size() - 1);         // Peek back
q.poll();          // Dequeue
q.length == 0;        // Check if empty
q.size();         // Get size
```

### Implement Queue using Stacks

```java
// import java.util.*;
class MyQueue {
    Deque<Integer> input, output;
    void push(int x) {
        input.offer(x);
    }

    int pop() {
        peek();
        int val = output.peek();
        output.poll();
        return val;
    }

    int peek() {
        if (output.length == 0) {
            while (!input.isEmpty()) {
                output.offer(input.peek());
                input.poll();
            }
        }
        return output.peek();
    }

    boolean empty() {
        return input.length == 0 && output.length == 0;
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 232 | Implement Queue using Stacks | [Link](https://leetcode.com/problems/implement-queue-using-stacks/) | - |

## BFS with Queue
**When to use:** "shortest path in unweighted graph", "level order traversal", "minimum steps", or any problem that explores neighbors layer by layer.

Queue is essential for Breadth-First Search (level-order traversal).



| ID | Title | Link | Solution |
|---|---|---|---|
| 102 | Binary Tree Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal/) | - |
| 107 | Binary Tree Level Order Traversal II | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) | - |

```java
// import java.util.*;
// BFS on graph
static void bfs(int[][] graph, int start) {
    Queue<Integer> q = new LinkedList<>();
    boolean[]visited(graph.size(), false);
    q.offer(start);
    visited[start] = true;

    while (!q.isEmpty()) {
        int node = q.get(0);
        q.poll();
        // Process node

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.offer(neighbor);
            }
        }
    }
}

// Level-order traversal (BFS on tree)
int[][] levelOrder(TreeNode root) {
    List<int[]> result = new ArrayList<>();
    if (!root) return result;

    Queue<TreeNode> q = new LinkedList<>();
    q.offer(root);

    while (!q.isEmpty()) {
        int size = q.size();
        List<Integer> level = new ArrayList<>();

        for (int i = 0; i < size; ++i) {
            TreeNode node = q.get(0);
            q.poll();
            level.add(node.val);

            if (node.left) q.offer(node.left);
            if (node.right) q.offer(node.right);
        }

        result.add(level);
    }

    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 102 | Binary Tree Level Order Traversal | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal/) | - |
| 107 | Binary Tree Level Order Traversal II | [Link](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/) | - |

## Monotonic Queue
**When to use:** "sliding window maximum/minimum", or when you need the max/min of every window of size k in O(n) total.

Maintain queue with monotonic property (increasing or decreasing).



| ID | Title | Link | Solution |
|---|---|---|---|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-239-sliding-window-maximum/) |
| 1438 | Longest Continuous Subarray With Absolute Diff <= Limit | [Link](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) | - |

```java
// import java.util.*;
// Monotonic decreasing queue (for sliding window maximum)
class MonotonicQueue {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    void push(int val) {
        // Remove elements smaller than val
        while (!dq.isEmpty() && dq.get(dq.size() - 1) < val) {
            dq.removeLast();
        }
        dq.add(val);
    }

    void pop(int val) {
        if (!dq.isEmpty() && dq.get(0) == val) {
            dq.removeFirst();
        }
    }

    int Math.max() {
        return dq.get(0);
    }
}
// Sliding Window Maximum
int[]maxSlidingWindow(int[] nums, int k) {
    MonotonicQueue mq;
    List<Integer> result = new ArrayList<>();

    for (int i = 0; i < nums.length; ++i) {
        if (i < k - 1) {
            mq.offer(nums[i]);
        } else {
            mq.offer(nums[i]);
            result.add(mq.Math.max());
            mq.pop(nums[i - k + 1]);
        }
    }

    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-239-sliding-window-maximum/) |
| 1438 | Longest Continuous Subarray With Absolute Diff <= Limit | [Link](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) | - |

## Priority Queue
**When to use:** "k-th largest/smallest", "merge k sorted lists", "top k elements", "schedule tasks by priority", or any problem needing efficient access to the current extreme value.

Priority queue (heap) for maintaining order.



### K-way Merge



### Top K Elements



| ID | Title | Link | Solution |
|---|---|---|---|
| 23 | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) | - |
| 347 | Top K Frequent Elements | [Link](https://leetcode.com/problems/top-k-frequent-elements/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-21-medium-347-top-k-frequent-elements/) |
| 295 | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) | - |
| 215 | Kth Largest Element in an Array | [Link](https://leetcode.com/problems/kth-largest-element-in-an-array/) | - |
| 973 | K Closest Points to Origin | [Link](https://leetcode.com/problems/k-closest-points-to-origin/) | - |
| 253 | Meeting Rooms II | [Link](https://leetcode.com/problems/meeting-rooms-ii/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-11-medium-253-meeting-rooms-ii/) |
| 378 | Kth Smallest Element in a Sorted Matrix | [Link](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | - |
| 703 | Kth Largest Element in a Stream | [Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | - |
| 767 | Reorganize String | [Link](https://leetcode.com/problems/reorganize-string/) | - |
| 1046 | Last Stone Weight | [Link](https://leetcode.com/problems/last-stone-weight/) | - |
| 1167 | Minimum Cost to Connect Sticks | [Link](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) | - |
| 621 | Task Scheduler | [Link](https://leetcode.com/problems/task-scheduler/) | - |
| 743 | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) | - |
| 787 | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | - |

```java
// import java.util.*;

// Max heap (default)
PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>();

// Min heap
PriorityQueue<Integer> minHeap;

// Custom comparator using class
class Compare {
    
}
PriorityQueue<int[]> pq;

// Custom comparator using lambda operator

PriorityQueue<int[]> pq(cmp);

// Lambda example: Min heap by distance (for Dijkstra's algorithm)
 - min heap by distance
}
PriorityQueue<int[]> pq(distCmp);
```

### K-way Merge

```java
// Merge k sorted lists using priority queue
ListNode mergeKLists(ListNode[] lists) {
    
    priority_queue<ListNode, ListNode[], > pq(cmp);

    for (ListNode list : lists) {
        if (list) pq.offer(list);
    }

    ListNode dummy = new ListNode = new new(0);
    ListNode cur = dummy;

    while (!pq.isEmpty()) {
        ListNode node = pq.peek();
        pq.poll();
        cur.next = node;
        cur = cur.next;
        if (node.next) pq.offer(node.next);
    }

    return dummy.next;
}
```

### Top K Elements

```java
// import java.util.*;
// Find top k frequent elements
int[]topKFrequent(int[] nums, int k) {
    HashMap<Integer, Integer> freq = new HashMap<Integer, Integer>();
    for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

    PriorityQueue<int[]> pq;

    for (var e : freq.entrySet()) {
        pq.offer(new int[] {count, num});
        if (pq.size() > k) pq.poll();
    }

    List<Integer> result = new ArrayList<>();
    while (!pq.isEmpty()) {
        result.add(pq.peek().second);
        pq.poll();
    }

    return result;
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 23 | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) | - |
| 347 | Top K Frequent Elements | [Link](https://leetcode.com/problems/top-k-frequent-elements/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-10-21-medium-347-top-k-frequent-elements/) |
| 295 | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) | - |
| 215 | Kth Largest Element in an Array | [Link](https://leetcode.com/problems/kth-largest-element-in-an-array/) | - |
| 973 | K Closest Points to Origin | [Link](https://leetcode.com/problems/k-closest-points-to-origin/) | - |
| 253 | Meeting Rooms II | [Link](https://leetcode.com/problems/meeting-rooms-ii/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-12-11-medium-253-meeting-rooms-ii/) |
| 378 | Kth Smallest Element in a Sorted Matrix | [Link](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | - |
| 703 | Kth Largest Element in a Stream | [Link](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | - |
| 767 | Reorganize String | [Link](https://leetcode.com/problems/reorganize-string/) | - |
| 1046 | Last Stone Weight | [Link](https://leetcode.com/problems/last-stone-weight/) | - |
| 1167 | Minimum Cost to Connect Sticks | [Link](https://leetcode.com/problems/minimum-cost-to-connect-sticks/) | - |
| 621 | Task Scheduler | [Link](https://leetcode.com/problems/task-scheduler/) | - |
| 743 | Network Delay Time | [Link](https://leetcode.com/problems/network-delay-time/) | - |
| 787 | Cheapest Flights Within K Stops | [Link](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | - |

## Circular Queue
**When to use:** "design a circular buffer", "design a queue with fixed capacity", or when you need wrap-around behavior with modulo arithmetic.



| ID | Title | Link | Solution |
|---|---|---|---|
| 622 | Design Circular Queue | [Link](https://leetcode.com/problems/design-circular-queue/) | - |

```java
class MyCircularQueue {
    List<Integer> data = new ArrayList<>();
        int head, tail, size, capacity;
    MyCircularQueue(int k) {}

    boolean enQueue(int value) {
        if (isFull()) return false;
        data[tail] = value;
        tail = (tail + 1) % capacity;
        size++;
        return true;
    }

    boolean deQueue() {
        if (isEmpty()) return false;
        head = (head + 1) % capacity;
        size--;
        return true;
    }

    int Front() {
        return isEmpty() ? -1 : data[head];
    }

    int Rear() {
        return isEmpty() ? -1 : data[(tail - 1 + capacity) % capacity];
    }

    boolean isEmpty() {
        return size == 0;
    }

    boolean isFull() {
        return size == capacity;
    }
}
```

| ID | Title | Link | Solution |
|---|---|---|---|
| 622 | Design Circular Queue | [Link](https://leetcode.com/problems/design-circular-queue/) | - |

## Double-ended Queue (Deque)
**When to use:** "sliding window" problems where you need to push/pop from both front and back, or when maintaining sorted order in a window by index.



### Sliding Window with Deque



### Two Deques Pattern (Middle Element Access)

Use two deques to efficiently access middle elements in a queue.



**Key points:**
- Split queue into two halves: `front_cache` and `back_cache`
- Maintain balance: `front_cache.size() <= back_cache.size() <= front_cache.size() + 1`
- Middle element is `front_cache.back()` (if sizes equal) or `back_cache.front()` (if back_cache larger)
- Rebalance after each modification

| ID | Title | Link | Solution |
|---|---|---|---|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-239-sliding-window-maximum/) |
| 1670 | Design Front Middle Back Queue | [Link](https://leetcode.com/problems/design-front-middle-back-queue/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/13/medium-1670-design-front-middle-back-queue/) |

```java
// import java.util.*;

ArrayDeque<Integer> dq = new ArrayDeque<>();
dq.push_front(1);  // Add to front
dq.add(2);   // Add to back
dq.removeFirst();     // Remove from front
dq.removeLast();      // Remove from back
dq.get(0);         // Access front
dq.get(dq.size() - 1);          // Access back
```

### Sliding Window with Deque

```java
// import java.util.*;
// Sliding window maximum using deque
int[]maxSlidingWindow(int[] nums, int k) {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    List<Integer> result = new ArrayList<>();

    for (int i = 0; i < nums.length; ++i) {
        // Remove indices outside window
        while (!dq.isEmpty() && dq.get(0) <= i - k) {
            dq.removeFirst();
        }

        // Remove indices with smaller values
        while (!dq.isEmpty() && nums[dq.get(dq.size() - 1)] <= nums[i]) {
            dq.removeLast();
        }

        dq.add(i);

        if (i >= k - 1) {
            result.add(nums[dq.get(0)]);
        }
    }

    return result;
}
```

### Two Deques Pattern (Middle Element Access)

Use two deques to efficiently access middle elements in a queue.

```java
// import java.util.*;
// Front Middle Back Queue: Two deques with rebalancing
class FrontMiddleBackQueue {
    ArrayDeque<Integer> front_cache, back_cache;

    void rebalance() {
        // Maintain: front_cache.size() <= back_cache.size() <= front_cache.size() + 1
        while(front_cache.size() > back_cache.size()) {
            back_cache.push_front(front_cache.get(front_cache.size() - 1));
            front_cache.removeLast();
        }
        while(back_cache.size() > front_cache.size() + 1) {
            front_cache.add(back_cache.get(0));
            back_cache.removeFirst();
        }
    }
    void pushMiddle(int val) {
        front_cache.add(val);
        rebalance();
    }

    int popMiddle() {
        if(front_cache.length == 0 && back_cache.length == 0) return -1;
        if(front_cache.size() == back_cache.size()) {
            int val = front_cache.get(front_cache.size() - 1);
            front_cache.removeLast();
            return val;
        } else {
            int val = back_cache.get(0);
            back_cache.removeFirst();
            return val;
        }
    }
}
```

**Key points:**
- Split queue into two halves: `front_cache` and `back_cache`
- Maintain balance: `front_cache.size() <= back_cache.size() <= front_cache.size() + 1`
- Middle element is `front_cache.back()` (if sizes equal) or `back_cache.front()` (if back_cache larger)
- Rebalance after each modification

| ID | Title | Link | Solution |
|---|---|---|---|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) | [Solution](https://robinali34.github.io/blog_leetcode_java/posts/2025-11-04-hard-239-sliding-window-maximum/) |
| 1670 | Design Front Middle Back Queue | [Link](https://leetcode.com/problems/design-front-middle-back-queue/) | [Solution](https://robinali34.github.io/blog_leetcode_java/2026/01/13/medium-1670-design-front-middle-back-queue/) |

## More templates
- **Data structures (monotonic queue):** [Data Structures & Core Algorithms](/posts/2025-10-29-leetcode-templates-data-structures/)
- **BFS, Graph:** [BFS](/posts/2025-11-24-leetcode-templates-bfs/), [Graph](/posts/2025-10-29-leetcode-templates-graph/)
- **Master index:** [Categories & Templates](/posts/2025-10-29-leetcode-categories-and-templates/)
{% endraw %}
