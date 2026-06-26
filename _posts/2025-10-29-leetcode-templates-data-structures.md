---
layout: post
title: "Algorithm Templates: Data Structures & Core Algorithms"
date: 2025-10-29 00:00:00 -0700
categories: leetcode templates data-structures algorithms
permalink: /posts/2025-10-29-leetcode-templates-data-structures/
tags: [leetcode, templates, data-structures, algorithms]
---

Minimal, copy-paste Java templates for common structures and patterns. Each snippet is self-contained and uses standard indexing.

## Contents

- [Binary Search (Bounds)](#binary-search-bounds)
- [Prefix Sum & Difference Array](#prefix-sum--difference-array)
- [Monotonic Stack](#monotonic-stack)
- [Monotonic Queue](#monotonic-queue)
- [Heap / Priority Queue](#heap--priority-queue)
- [Union-Find (DSU)](#union-find-dsu)
- [Trie](#trie)
- [Segment Tree](#segment-tree)
- [Fenwick Tree (BIT)](#fenwick-tree-bit)
- [Sparse Table (Range Min/Max)](#sparse-table-range-minmax)

---

## Binary Search (Bounds)

Half-open range `[lo, hi)`. Use when you need first ≥ x (binary search (lower bound)) or first > x (binary search (upper bound)).

```java
// First index where a[i] >= x (floorKey)
static int floorKey(int[] a, int x) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// First index where a[i] > x (binary search (upper bound))
static int binary search (upper bound)(int[] a, int x) {
    int lo = 0, hi = a.size();
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

// Binary search on answer: smallest x in [lo, hi] such that ok(x)
template<class F>
static int bsearch_ans(int lo, int hi, F ok) {
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (ok(mid)) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}
```

| ID | Title | Link |
|----|--------|------|
| 34 | Find First and Last Position | [Link](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) |
| 35 | Search Insert Position | [Link](https://leetcode.com/problems/search-insert-position/) |
| 875 | Koko Eating Bananas | [Link](https://leetcode.com/problems/koko-eating-bananas/) |

---

## Prefix Sum & Difference Array

Prefix sum: range sum in O(1). Difference array: range add in O(1), then one prefix sum to recover.

```java
// Prefix sum: ps[i] = a[0]+...+a[i-1], sum(l,r) = ps[r+1]-ps[l]
long[]prefix(int[] a) {
    long[]ps(a.size() + 1);
    for (int i = 0; i < (int)a.size(); i++) ps[i + 1] = ps[i] + a[i];
    return ps;
}

// Difference array: for [l,r] += d do diff.put(l, diff.getOrDefault(l, 0) + d, diff[r+1]-=d; then partial_sum(diff) = values
static void range_add(long[] diff, int l, int r, long d) {
    diff.put(l, diff.getOrDefault(l, 0) + d;
    if (r + 1 < (int)diff.size()) diff[r + 1] -= d;
}
// After all updates: partial_sum(diff /* elements of diff */, diff.iterator());
```

| ID | Title | Link |
|----|--------|------|
| 560 | Subarray Sum Equals K | [Link](https://leetcode.com/problems/subarray-sum-equals-k/) |
| 1109 | Corporate Flight Bookings | [Link](https://leetcode.com/problems/corporate-flight-bookings/) |
| 1094 | Car Pooling | [Link](https://leetcode.com/problems/car-pooling/) |

---

## Monotonic Stack

Maintain indices with strictly increasing (or decreasing) values. Use for next greater/smaller, or histogram rectangle.

```java
// Next greater element (for each index)
int[]next_greater(int[] a) {
    int n = a.size();
    int[]ng(n, -1);
    List<Integer> st = new ArrayList<>();
    for (int i = 0; i < n; i++) {
        while (!st.isEmpty() && a[st.get(st.size() - 1)] < a[i]) {
            ng[st.get(st.size() - 1)] = a[i];
            st.removeLast();
        }
        st.add(i);
    }
    return ng;
}

// Circular: wrap with 2 n and only push when i < n
int[]next_greater_circular(int[] a) {
    int n = a.size();
    int[]ng(n, -1);
    List<Integer> st = new ArrayList<>();
    for (int i = 0; i < 2 n; i++) {
        int j = i % n;
        while (!st.isEmpty() && a[st.get(st.size() - 1)] < a[j]) {
            ng[st.get(st.size() - 1)] = a[j];
            st.removeLast();
        }
        if (i < n) st.add(j);
    }
    return ng;
}
```

| ID | Title | Link |
|----|--------|------|
| 739 | Daily Temperatures | [Link](https://leetcode.com/problems/daily-temperatures/) |
| 42 | Trapping Rain Water | [Link](https://leetcode.com/problems/trapping-rain-water/) |
| 84 | Largest Rectangle in Histogram | [Link](https://leetcode.com/problems/largest-rectangle-in-histogram/) |
| 503 | Next Greater Element II | [Link](https://leetcode.com/problems/next-greater-element-ii/) |
| 1944 | Visible People in Queue | [Link](https://leetcode.com/problems/number-of-visible-people-in-a-queue/) |

---

## Monotonic Queue

Deque of indices with values in monotonic order. Sliding window max/min.

```java
// import java.util.*;
// Sliding window maximum (window size k)
int[]max_sliding_window(int[] a, int k) {
    ArrayDeque<Integer> dq = new ArrayDeque<>();
    List<Integer> out = new ArrayList<>();
    for (int i = 0; i < (int)a.size(); i++) {
        while (!dq.isEmpty() && a[dq.get(dq.size() - 1)] <= a[i]) dq.removeLast();
        dq.add(i);
        if (dq.get(0) <= i - k) dq.removeFirst();
        if (i >= k - 1) out.add(a[dq.get(0)]);
    }
    return out;
}
```

| ID | Title | Link |
|----|--------|------|
| 239 | Sliding Window Maximum | [Link](https://leetcode.com/problems/sliding-window-maximum/) |
| 1438 | Longest Continuous Subarray With Abs Diff ≤ Limit | [Link](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) |

---

## Heap / Priority Queue

Min-heap: `PriorityQueue<T>` with comparator. K-way merge: push heads, pop min, push next from same list.

```java
// K-way merge of sorted arrays (or list heads)
int[]merge_k_sorted(int[][] lists) {
    
    priority_queue<T, T[], greater<T>> pq;
    for (int i = 0; i < (int)lists.size(); i++)
        if (!lists[i].empty()) pq.emplace(lists[i][0], i, 0);
    List<Integer> out = new ArrayList<>();
    while (!pq.isEmpty()) {
        auto [v, i, j] = pq.peek();
        pq.poll();
        out.add(v);
        if (j + 1 < (int)lists[i].size()) pq.emplace(lists[i][j + 1], i, j + 1);
    }
    return out;
}
```

| ID | Title | Link |
|----|--------|------|
| 23 | Merge k Sorted Lists | [Link](https://leetcode.com/problems/merge-k-sorted-lists/) |
| 295 | Find Median from Data Stream | [Link](https://leetcode.com/problems/find-median-from-data-stream/) |

---

## Union-Find (DSU)

Path compression + rank merge. `find(x)`, `unite(a,b)`.

```java
class DSU {
    int[]p, r;
    DSU(int n) { iota(p /* elements of p */, 0); }
    int find(int x) { return p[x] == x ? x : p[x] = find(p[x]); }
    boolean unite(int a, int b) {
        a = find(a), b = find(b);
        if (a == b) return false;
        if (r[a] < r[b]) swap(a, b);
        p[b] = a;
        if (r[a] == r[b]) r.put(a, r.getOrDefault(a, 0) + 1);
        return true;
    }
}
```

| ID | Title | Link |
|----|--------|------|
| 684 | Redundant Connection | [Link](https://leetcode.com/problems/redundant-connection/) |
| 721 | Accounts Merge | [Link](https://leetcode.com/problems/accounts-merge/) |
| 1319 | Number of Operations to Make Network Connected | [Link](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) |

---

## Trie

Fixed alphabet (e.g. 26). Insert and search in O(|s|).

```java
class Trie {
    class Node {
        int[] nxt = new int[26];
        boolean end = false;
        Node() { memset(nxt, -1, sizeof nxt); }
    }
    Node[]t{1}
    public void insert(String s) {
        int u = 0;
        for (char c : s.toCharArray()) {
            int i = c - 'a';
            if (t.charAt(u).nxt[i] == -1) { t.charAt(u).nxt[i] = t.size(); t.add(); }
            u = t.charAt(u).nxt[i];
        }
        t.charAt(u).end = true;
    }
        public boolean search(String s) {
        int u = 0;
        for (char c : s.toCharArray()) {
            u = t.charAt(u).nxt[c - 'a'];
            if (u == -1) return false;
        }
        return t.charAt(u).end;
    }
}
```

| ID | Title | Link |
|----|--------|------|
| 208 | Implement Trie | [Link](https://leetcode.com/problems/implement-trie-prefix-tree/) |
| 211 | Design Add and Search Words | [Link](https://leetcode.com/problems/design-add-and-search-words-data-structure/) |
| 212 | Word Search II | [Link](https://leetcode.com/problems/word-search-ii/) |

---

## Segment Tree

0-indexed range [0, n-1]. Point update, range sum (or min/max). Recursive implementation.

```java
class SegTree {
        int n;
    long[]st;
    SegTree(int n) {}
    void upd(int i, int l, int r, int p, long v) {
        if (l == r) { st[i] = v; return; }
        int m = (l + r) / 2;
        if (p <= m) upd(2 i, l, m, p, v);
        else upd = new else(2 i + 1, m + 1, r, p, v);
        st[i] = st[2 i] + st[2 i + 1];
    }
    long qry(int i, int l, int r, int ql, int qr) {
        if (qr < l || r < ql) return 0;
        if (ql <= l && r <= qr) return st[i];
        int m = (l + r) / 2;
        return qry(2 i, l, m, ql, qr) + qry(2 i + 1, m + 1, r, ql, qr);
    }
    void upd(int p, long v) { upd(1, 0, n - 1, p, v); }
    long qry(int ql, int qr) { return qry = new return(1, 0, n - 1, ql, qr); }
}
```

| ID | Title | Link |
|----|--------|------|
| 307 | Range Sum Query – Mutable | [Link](https://leetcode.com/problems/range-sum-query-mutable/) |
| 732 | My Calendar III | [Link](https://leetcode.com/problems/my-calendar-iii/) |

---

## Fenwick Tree (BIT)

1-indexed. Point add, prefix sum. Range sum [l, r] = sum(r) - sum(l-1).

```java
class BIT {
        int n;
    long[]f;
    BIT(int n) {}
    void add(int i, long v) {
        for (; i <= n; i += i & -i) f.put(i, f.getOrDefault(i, 0) + v;
    }
    long sum(int i) {
        long s = 0;
        for (; i > 0; i -= i & -i) s += f[i];
        return s;
    }
    long range_sum(int l, int r) { return sum(r) - sum(l - 1); }
}
```

| ID | Title | Link |
|----|--------|------|
| 307 | Range Sum Query – Mutable | [Link](https://leetcode.com/problems/range-sum-query-mutable/) |
| 315 | Count of Smaller Numbers After Self | [Link](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) |
| 308 | Range Sum Query 2D – Mutable | [Link](https://leetcode.com/problems/range-sum-query-2d-mutable/) |

---

## Sparse Table (Range Min/Max)

O(n log n) build, O(1) range min/max. Idempotent only (min, max, gcd). 0-indexed.

```java
class SparseTable {
    List<int[]> st = new ArrayList<>();
    List<Integer> lg = new ArrayList<>();
    int op(int a, int b) { return Math.min(a, b); } // or max
    SparseTable(int[] a) {
        int n = a.size();
        lg.assign(n + 1, 0);
        for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
        int k = lg[n] + 1;
        st.assign(n, int[](k));
        for (int i = 0; i < n; i++) st[i][0] = a[i];
        for (int j = 1; j < k; j++)
            for (int i = 0; i + (1 << j) <= n; i++)
                st[i][j] = op(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
    }
    int qry(int l, int r) {
        int j = lg[r - l + 1];
        return op(st[l][j], st[r - (1 << j) + 1][j]);
    }
}
```

| ID | Title | Link |
|----|--------|------|
| — | Range min/max, GCD (no update) | — |

---

## More Templates

- **Graph (BFS, Dijkstra, Topo, DSU):** [Graph Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-templates-graph/)
- **Binary search (rotated, 2D, answer space):** [Search Templates](/blog_leetcode_java/posts/2026-01-20-leetcode-templates-search/)
- **DP, Backtracking, Greedy, Stack:** [Categories & Templates](/blog_leetcode_java/posts/2025-10-29-leetcode-categories-and-templates/)
