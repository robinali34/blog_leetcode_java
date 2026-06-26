#!/usr/bin/env python3
"""Rewrite heap template post with valid Java code blocks."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "_posts/2026-01-05-leetcode-templates-heap.md"

JAVA_BLOCKS = {
    "min_heap_basic": """// Min heap (smallest element at top)
PriorityQueue<Integer> minHeap = new PriorityQueue<>();

// Basic operations
minHeap.offer(5);
minHeap.offer(2);
minHeap.offer(8);
minHeap.offer(1);

minHeap.peek();    // Returns 1 (smallest)
minHeap.poll();    // Removes 1
minHeap.peek();    // Returns 2 (next smallest)""",

    "find_k_smallest": """int[] findKSmallest(int[] nums, int k) {
    PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    for (int num : nums) minHeap.offer(num);
    int[] result = new int[k];
    for (int i = 0; i < k && !minHeap.isEmpty(); i++) {
        result[i] = minHeap.poll();
    }
    return result;
}""",

    "max_heap_basic": """// Max heap (largest element at top)
PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());

maxHeap.offer(5);
maxHeap.offer(2);
maxHeap.offer(8);
maxHeap.offer(1);

maxHeap.peek();    // Returns 8 (largest)
maxHeap.poll();    // Removes 8
maxHeap.peek();    // Returns 5 (next largest)""",

    "find_k_largest": """int[] findKLargest(int[] nums, int k) {
    PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
    for (int num : nums) maxHeap.offer(num);
    int[] result = new int[k];
    for (int i = 0; i < k && !maxHeap.isEmpty(); i++) {
        result[i] = maxHeap.poll();
    }
    return result;
}""",

    "comparator_pairs": """// Min heap by second element (frequency)
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[] {1, 5});
pq.offer(new int[] {2, 3});
pq.offer(new int[] {3, 7});
pq.peek(); // {2, 3}""",

    "comparator_node": """record Node(int cost, int id) {}
PriorityQueue<Node> pq = new PriorityQueue<>(Comparator.comparingInt(n -> n.cost));
pq.offer(new Node(10, 1));
pq.offer(new Node(5, 2));
pq.peek(); // Node(5, 2)""",

    "lambda_dist": """PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
pq.offer(new int[] {10, 0});
pq.offer(new int[] {5, 1});
pq.peek(); // {5, 1}""",

    "point_compare": """record Point(int x, int y) {
    int distSq() { return x * x + y * y; }
}
PriorityQueue<Point> pq = new PriorityQueue<>(Comparator.comparingInt(Point::distSq));""",

    "keep_k_largest": """PriorityQueue<Integer> minHeap = new PriorityQueue<>();
for (int num : nums) {
    minHeap.offer(num);
    if (minHeap.size() > k) minHeap.poll();
}""",

    "top_k_freq_pattern": """Map<Integer, Integer> freq = new HashMap<>();
for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);
PriorityQueue<int[]> minHeap = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
for (var e : freq.entrySet()) {
    minHeap.offer(new int[] {e.getValue(), e.getKey()});
    if (minHeap.size() > k) minHeap.poll();
}""",

    "merge_k_lists": """ListNode mergeKLists(ListNode[] lists) {
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
}""",

    "merge_k_arrays": """int[] mergeKSortedArrays(int[][] arrays) {
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
}""",

    "top_k_frequent": """int[] topKFrequent(int[] nums, int k) {
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
}""",

    "k_closest": """int[][] kClosest(int[][] points, int k) {
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
}""",

    "kth_largest_heap": """class Solution {
    public int findKthLargest(int[] nums, int k) {
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int num : nums) {
            minHeap.offer(num);
            if (minHeap.size() > k) minHeap.poll();
        }
        return minHeap.peek();
    }
}""",

    "kth_largest_quickselect": """class Solution {
    public int findKthLargest(int[] nums, int k) {
        return quickSelect(nums, 0, nums.length - 1, nums.length - k);
    }

    private int quickSelect(int[] nums, int l, int r, int k) {
        if (l == r) return nums[k];
        int pivot = nums[l], i = l - 1, j = r + 1;
        while (i < j) {
            while (nums[++i] < pivot);
            while (nums[--j] > pivot);
            if (i < j) { int t = nums[i]; nums[i] = nums[j]; nums[j] = t; }
        }
        if (k <= j) return quickSelect(nums, l, j, k);
        return quickSelect(nums, j + 1, r, k);
    }
}""",

    "median_finder": """class MedianFinder {
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
}""",

    "sliding_window_median_note": """// Sliding window median (LC 480) typically uses two balanced heaps
// or a TreeMultiset-style structure. See the dedicated LC 480 post for a full solution.""",

    "dijkstra": """int[] dijkstra(List<List<int[]>> graph, int start) {
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
}""",
}


def fence(code: str) -> str:
    return f"```java\n{code}\n```"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    # Replace from Min Heap section through Dijkstra section
    start = text.index("## Min Heap")
    end = text.index("## Easy Problems")
    new_body = """## Min Heap

Min heap keeps the smallest element at the top.

""" + fence(JAVA_BLOCKS["min_heap_basic"]) + """

### Example: Find K Smallest Elements

""" + fence(JAVA_BLOCKS["find_k_smallest"]) + """

## Max Heap

Max heap keeps the largest element at the top (default in C++; use `Comparator.reverseOrder()` in Java).

""" + fence(JAVA_BLOCKS["max_heap_basic"]) + """

### Example: Find K Largest Elements

""" + fence(JAVA_BLOCKS["find_k_largest"]) + """

## Custom Comparators

### Pair Comparator

""" + fence(JAVA_BLOCKS["comparator_pairs"]) + """

### Custom Object Comparator

""" + fence(JAVA_BLOCKS["comparator_node"]) + """

### Distance Comparator (Dijkstra)

""" + fence(JAVA_BLOCKS["lambda_dist"]) + """

### Point Comparator

""" + fence(JAVA_BLOCKS["point_compare"]) + """

## Common Patterns

### Pattern 1: Maintain K Elements

""" + fence(JAVA_BLOCKS["keep_k_largest"]) + """

### Pattern 2: Frequency-Based

""" + fence(JAVA_BLOCKS["top_k_freq_pattern"]) + """

## K-way Merge

""" + fence(JAVA_BLOCKS["merge_k_lists"]) + """

### K-way Merge for Arrays

""" + fence(JAVA_BLOCKS["merge_k_arrays"]) + """

## Top K Elements

### Top K Frequent Elements

""" + fence(JAVA_BLOCKS["top_k_frequent"]) + """

### K Closest Points to Origin

""" + fence(JAVA_BLOCKS["k_closest"]) + """

### Kth Largest Element in an Array (LC 215)

**Solution 1: Min Heap (O(n log k))**

""" + fence(JAVA_BLOCKS["kth_largest_heap"]) + """

**Solution 2: QuickSelect (O(n) average)**

""" + fence(JAVA_BLOCKS["kth_largest_quickselect"]) + """

## Two Heaps

### Find Median from Data Stream

""" + fence(JAVA_BLOCKS["median_finder"]) + """

### Sliding Window Median

""" + fence(JAVA_BLOCKS["sliding_window_median_note"]) + """

## Dijkstra's Algorithm

""" + fence(JAVA_BLOCKS["dijkstra"]) + """

"""
    updated = text[:start] + new_body + text[end:]
    TARGET.write_text(updated, encoding="utf-8")
    print("Rewrote heap template Java blocks")


if __name__ == "__main__":
    main()
