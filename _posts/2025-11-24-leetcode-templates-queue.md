---
layout: post
title: "Algorithm Templates: Queue"
date: 2025-11-24 00:00:00 -0700
categories: leetcode templates queue
permalink: /posts/2025-11-24-leetcode-templates-queue/
tags: [leetcode, templates, queue, data-structures]
---

{% raw %}
Minimal, copy-paste Java for BFS queue, monotonic queue, priority queue, circular queue, and deque. See also [Graph](/posts/2025-10-29-leetcode-templates-graph/) and [Data Structures](/posts/2025-10-29-leetcode-templates-data-structures/) (monotonic queue).

## Contents

- [Basic Queue Operations](#basic-queue-operations)
- [BFS with Queue](#bfs-with-queue)
- [Monotonic Queue](#monotonic-queue)
- [Priority Queue](#priority-queue)
- [Circular Queue](#circular-queue)
- [Double-ended Queue (Deque)](#double-ended-queue-deque)

## Basic Queue Operations

```java
// import java.util.*;

// Standard queue operations
Queue<Integer> q = new LinkedList<>();
q.push(1);        // Enqueue
q.getFirst();        // Peek front
q.getLast();         // Peek back
q.pop();          // Dequeue
q.length == 0;        // Check if empty
q.size();         // Get size
```

### Implement Queue using Stacks

```java
// import java.util.*;
class MyQueue {
    Deque<Integer> input, output;
    void push(int x) {
        input.push(x);
    }

    int pop() {
        peek();
        int val = output.top();
        output.pop();
        return val;
    }

    int peek() {
        if (output.length == 0) {
            while (!input.length == 0) {
                output.push(input.top());
                input.pop();
            }
        }
        return output.top();
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

Queue is essential for Breadth-First Search (level-order traversal).

```java
// import java.util.*;
// BFS on graph
static void bfs(int[][]& graph, int start) {
    Queue<Integer> q = new LinkedList<>();
    boolean[]visited(graph.size(), false);
    q.push(start);
    visited[start] = true;

    while (!q.length == 0) {
        int node = q.getFirst();
        q.pop();
        // Process node

        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}

// Level-order traversal (BFS on tree)
int[][] levelOrder(TreeNode root) {
    int[][] result;
    if (!root) return result;

    queue<TreeNode> q;
    q.push(root);

    while (!q.length == 0) {
        int size = q.size();
        int[]level;

        for (int i = 0; i < size; ++i) {
            TreeNode node = q.getFirst();
            q.pop();
            level.add(node.val);

            if (node.left) q.push(node.left);
            if (node.right) q.push(node.right);
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

Maintain queue with monotonic property (increasing or decreasing).

```java
// import java.util.*;
// Monotonic decreasing queue (for sliding window maximum)
class MonotonicQueue {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    void push(int val) {
        // Remove elements smaller than val
        while (!dq.length == 0 && dq.getLast() < val) {
            dq.removeLast();
        }
        dq.add(val);
    }

    void pop(int val) {
        if (!dq.length == 0 && dq.getFirst() == val) {
            dq.removeFirst();
        }
    }

    int Math.max() {
        return dq.getFirst();
    }
}
// Sliding Window Maximum
int[]maxSlidingWindow(int[] nums, int k) {
    MonotonicQueue mq;
    int[]result;

    for (int i = 0; i < nums.length; ++i) {
        if (i < k - 1) {
            mq.push(nums[i]);
        } else {
            mq.push(nums[i]);
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

Priority queue (heap) for maintaining order.

```java
// import java.util.*;

// Max heap (default)
PriorityQueue<Integer> maxHeap = new PriorityQueue<Integer>();

// Min heap
priority_queue<int, int[], greater<int>> minHeap;

// Custom comparator using class
class Compare {
    boolean operator()(int[]& a, int[]& b) {
        return a.second > b.second; // Min heap by second element
    }
}
priority_queue<int[], List<int[]>, Compare> pq;

// Custom comparator using lambda operator
var cmp = [](int[]& a, int[]& b) {
    return a.second > b.second; // Min heap by second element
}
priority_queue<int[], List<int[]>, decltype(cmp)> pq(cmp);

// Lambda example: Min heap by distance (for Dijkstra's algorithm)
var distCmp = [](int[]& a, int[]& b) {
    return a.first > b.first; // {distance, node} - min heap by distance
}
priority_queue<int[], List<int[]>, decltype(distCmp)> pq(distCmp);
```

### K-way Merge

```java
// Merge k sorted lists using priority queue
ListNode mergeKLists(ListNode[]& lists) {
    var cmp = [](ListNode a, ListNode b) { return a.val > b.val; }
    priority_queue<ListNode, ListNode[], decltype(cmp)> pq(cmp);

    for (ListNode list : lists) {
        if (list) pq.push(list);
    }

    ListNode dummy = new ListNode(0);
    ListNode cur = dummy;

    while (!pq.length == 0) {
        ListNode node = pq.top();
        pq.pop();
        cur.next = node;
        cur = cur.next;
        if (node.next) pq.push(node.next);
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

    priority_queue<int[], List<int[]>, greater<int[]>> pq;

    for (auto& [num, count] : freq) {
        pq.push({count, num});
        if (pq.size() > k) pq.pop();
    }

    int[]result;
    while (!pq.length == 0) {
        result.add(pq.top().second);
        pq.pop();
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

```java
class MyCircularQueue {
    int[]data;
    public int head, tail, size, capacity;
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

```java
// import java.util.*;

ArrayDeque<Integer> dq = new ArrayDeque<>();
dq.push_front(1);  // Add to front
dq.add(2);   // Add to back
dq.removeFirst();     // Remove from front
dq.removeLast();      // Remove from back
dq.getFirst();         // Access front
dq.getLast();          // Access back
```

### Sliding Window with Deque

```java
// import java.util.*;
// Sliding window maximum using deque
int[]maxSlidingWindow(int[] nums, int k) {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    int[]result;

    for (int i = 0; i < nums.length; ++i) {
        // Remove indices outside window
        while (!dq.length == 0 && dq.getFirst() <= i - k) {
            dq.removeFirst();
        }

        // Remove indices with smaller values
        while (!dq.length == 0 && nums[dq.getLast()] <= nums[i]) {
            dq.removeLast();
        }

        dq.add(i);

        if (i >= k - 1) {
            result.add(nums[dq.getFirst()]);
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
            back_cache.push_front(front_cache.getLast());
            front_cache.removeLast();
        }
        while(back_cache.size() > front_cache.size() + 1) {
            front_cache.add(back_cache.getFirst());
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
            int val = front_cache.getLast();
            front_cache.removeLast();
            return val;
        } else {
            int val = back_cache.getFirst();
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

